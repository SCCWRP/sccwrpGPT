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
from flask import Flask, request, send_from_directory, render_template, redirect, send_file, session, jsonify, url_for

# sqlalchemy v1.4.15
from sqlalchemy import create_engine

# openai v1.9.0
from openai import OpenAI

# requests v2.25.1
import requests

# ----------------- Custom Imports ----------------- #
from utils.db import get_database_info, ask_database





# -------------------- Main App -------------------- #

app = Flask(__name__)

GPT_MODEL = os.getenv("GPT_MODEL")
assert GPT_MODEL is not None, "GPT_MODEL not defined in the environment variables"


@app.route('/', methods=['GET','POST'])
def test():
    return redirect(url_for('app.chat'))

@app.route("/chat", methods=['GET','POST'])
def chat():
    return render_template('chat.jinja2')

@app.route('/submit', methods=['POST'])
def submit():
    
    # A simple check for debugging, making it easier to resolve potenntial issues
    assert str(os.environ.get("DB_PORT", "")).isdigit(), "DB_PORT environment variable must be an integer value"
    
    print(request.json)
    data = request.json
    print(data["question"])
    question = data["question"]
    print("Here is the question:" + question)

    conn2= psycopg2.connect(
        database=os.getenv("DB_NAME"), 
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"), 
        host=os.getenv("DB_HOST"), 
        port=os.getenv("DB_PORT")
    )
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    client = OpenAI(
        # This is the default and can be omitted <---- this was Paul (and/or ChatGPT)'s comment, i am not sure what it means
        api_key=api_key
    )
    
    # GPT_MODEL is defined up top
    MODEL = GPT_MODEL
    database_schema_dict = get_database_info(conn2)
    database_schema_string = "\n".join(
            [
                f"Table: {table['table_name']}\nColumns: {', '.join(table['column_names'])}"
                for table in database_schema_dict
            ]
    )
    tools = [
    {
        "type": "function",
        "function": {
            "name": "ask_database",
            "description": "Use this function to answer user questions about chemistry, fish, infauan, and invertebrates in the Southern California Bight. Input should be a fully formed SQL query.",
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
    messages = []
    messages.append({"role": "system", "content": "Answer user questions by generating SQL queries against the Unified Database."})
    messages.append({"role": "user", "content": question})
    chat_response = client.chat.completions.create(model=GPT_MODEL, messages=messages, tools=tools, tool_choice="auto")
    tmp_message = str(chat_response.choices[0].message.model_dump_json())
    assistant_message = json.loads(tmp_message)
    assistant_message['content'] = assistant_message["tool_calls"][0]["function"]
    messages.append(assistant_message)
    if assistant_message.get("tool_calls"):
        results = execute_function_call(conn2,assistant_message)
        messages.append({"role": "tool", "tool_call_id": assistant_message["tool_calls"][0]['id'], "name": assistant_message["tool_calls"][0]["function"]["name"], "content": results})
    message_string = str(messages)
    conn2.close()
    return jsonify({'message': 'Data received: Question = {}'.format(messages)})
