# Original simple skeleton for the application was developed by Paul with his own platform.openai.com account
# The server was running Debian 10, and python 3.8.8 was installed

# He used the openai API for Python, version 1.9.0

# I will be listing the verisons for other libraries that were installed on the server on which the original app was running 
#    this way we can specify for the docker container

# These version numbers may not necessarily remain the same
# Above the imports i am simply noting the version that was on the previous server


# PSL Imports
import os, json 


# ----------------- Installed libs ----------------- #
# psycopg2 v2.9.3
import psycopg2 

# pandas v1.2.4 
import pandas as pd

# flask v1.1.2
from flask import Flask, request, send_from_directory, render_template, redirect, send_file, session, jsonify, url_for, g

# sqlalchemy v1.4.15
from sqlalchemy import create_engine

# openai v1.9.0
from openai import OpenAI, NotFoundError

# requests v2.25.1
import requests

# ----------------- Custom Imports ----------------- #
from utils.db import get_db_info, execute_function_call
from utils.api import get_query
from utils.json import CustomJSONEncoder




# -------------------------------- Main App -------------------------------- #

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_APP_SECRET_KEY")


# ----- Globals ----- #


# set the database connection string, database, and type of database we are going to point our application at
@app.before_request
def before_request():
    
    # A simple check for debugging, making it easier to resolve potenntial issues
    assert str(os.environ.get("DB_PORT", "")).isdigit(), "DB_PORT environment variable must be an integer value"
     
    # Keep the psycopg2 connection alive
    # g.dbconn = psycopg2.connect(
    #     database=os.getenv("DB_NAME"), 
    #     user=os.getenv("DB_USER"), 
    #     password=os.getenv("DB_PASSWORD"), 
    #     host=os.getenv("DB_HOST"), 
    #     port=os.getenv("DB_PORT")
    # )
    
    # use sqlalchemy eng only for the schema info
    g.eng = create_engine(
        f"postgresql://{os.environ.get('DB_USER','')}:{os.environ.get('DB_PASSWORD','')}@{os.environ.get('DB_HOST','')}:{os.environ.get('DB_PORT','')}/{os.environ.get('DB_NAME','')}"
    )
    
    # Set up the interaction with the chat GPT Assistants API
    g.gpt_model = os.getenv("GPT_MODEL")
    assert g.gpt_model is not None, "GPT_MODEL not defined in the environment variables"
    
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPENAI_API_KEY not defined in the environment variables"
    
    g.client = OpenAI(api_key=api_key)

    
    
    if session.get('ASSISTANT_ID') is None:
        
        
        db_schema_info = get_db_info(g.eng)
        
        database_schema_string = "\n".join(
            [
                f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
                for table in db_schema_info
            ]
        )
    
        # The tool / function that generates the SQL Query
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "ask_database",
                    "description": "Use this function to answer user questions about chemistry, fish, infauna, and invertebrates in the Southern California Bight. Input should be a fully formed SQL query.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": f"""
                                        SQL query extracting info to answer the user's question.
                                        SQL should be written using this database schema:
                                        {database_schema_string}
                                        The query should be returned in plain text, not in JSON.
                                        """,
                            }
                        },
                        "required": ["query"],
                    },
                }
            }
        ]
        assistant = g.client.beta.assistants.create(
            name="Data search",
            description="You are to receive database table and column information and generate SQL queries to retrieve data that the user asks for",
            instructions="Answer user questions by generating SQL queries against the Unified Database. You should also consider whether the tool output would give the user the data they want. They may send you further messages to refine the query.",
            model=g.gpt_model,
            tools=tools
        )
        session['ASSISTANT_ID'] = assistant.id
        

    if session.get('THREAD_ID') is None:
        thread = g.client.beta.threads.create()
        session['THREAD_ID'] = thread.id
    
    

@app.teardown_request
def teardown_request(exception):
    
    if hasattr(g, 'dbconn'):
        g.dbconn.close()
        
    if hasattr(g, 'eng'):
        g.eng.dispose()
        
    # if hasattr(g, 'client'):
        
    #     # Remove session thread
    #     if session.get('THREAD_ID') is not None:
    #         try:
    #             g.client.beta.threads.delete(session.get('THREAD_ID'))
    #         except NotFoundError:
    #             print(f"Thread {session.get('THREAD_ID')} not found")
    #         session.pop('THREAD_ID', None)
        
    #     # Remove session assistant
    #     if session.get('ASSISTANT_ID') is not None:
    #         try:
    #             g.client.beta.assistants.delete(session.get('ASSISTANT_ID'))
    #         except NotFoundError:
    #             print(f"Assistant {session.get('ASSISTANT_ID')} not found")
    #         session.pop('ASSISTANT_ID', None)

        

#  ---------------- Routes ---------------- #

@app.route("/", methods=['GET','POST'])
def chat():
    return render_template('search.jinja2')

@app.route('/submit', methods=['POST'])
def submit():
    
    # get info for the interaction with the chat gpt assistants api
    client = g.client
    THREAD_ID = session.get('THREAD_ID')
    ASSISTANT_ID = session.get('ASSISTANT_ID')
    
    # Get the user's question
    data = request.json
    QUESTION = data["question"]
    
    sql = get_query(client=client, assistant_id=ASSISTANT_ID, thread_id=THREAD_ID, user_prompt=QUESTION)
    
    if sql != '':
        print('sql')
        print(sql)
        try:
            # Run the query
            qryresult = pd.read_sql(sql.replace('%', '%%'), g.eng)
            
            print('qryresult')
            print(qryresult)
        
            # Convert to dict and then to JSON using the custom encoder
            qryresult_json = json.dumps(qryresult.to_dict('records'), cls=CustomJSONEncoder)
        
            return jsonify({'message': f'SQL: {sql}\nResult:{qryresult_json}'})
        
        except Exception as e:
            print("Exception occurred:")
            print(e)
            return jsonify({'message': f'SQL: {sql}\ERROR:{str(e)}'})

    
    # In this case, the assistant decided not to run the function and generate SQL
    # Get all messages from the thread once run is complete
    messages = client.beta.threads.messages.list(thread_id=THREAD_ID)

    assistant_responses = [msg for msg in messages.data if msg.role == 'assistant']

    resp = ''
    if len(assistant_responses) > 0:
        msg = assistant_responses[0]
        # There should be only one response so we return on first iteration
        for c in msg.content:
            resp = c.text.value
            
            print('message output:')
            print(resp)

        
    return jsonify({'message': resp})
