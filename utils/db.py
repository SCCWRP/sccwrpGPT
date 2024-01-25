import pandas as pd
import json

def get_db_info(eng):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    # Assuming `conn2` is your database connection
    df = pd.read_sql( "SELECT table_name, column_name FROM information_schema.columns WHERE table_name LIKE 'tbl%%unifiedpublish';", eng )
    
    # Grouping columns by table
    grouped = df.groupby('table_name')['column_name'].apply(list)
    
    # Creating the list of dictionaries
    tables_columns = [{'table_name': table, 'column_names': columns} for table, columns in grouped.items()]
    
    # `tables_columns` now contains your desired structure
    return tables_columns



def ask_database(conn, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        cursor3 = conn.cursor()
        results_query = str(cursor3.execute(query))
        results = cursor3.fetchall()
    except Exception as e:
        results = f"query failed with error: {e}"
    return results

def execute_function_call(conn, message):
    if message["tool_calls"][0]["function"]["name"] == "ask_database":
        query = json.loads(message["tool_calls"][0]["function"]["arguments"])["query"]
        results = ask_database(conn, query)
    else:
        results = f"Error: function {message['tool_calls'][0]['function']['name']} does not exist"
    return results