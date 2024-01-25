def get_postgres_table_names(conn2):
    #print(conn2)
    cursor = conn2.cursor()
    #print(cursor)
    """Return a list of table names."""
    table_names = []
    tables = cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='sde' and table_name like 'tbl%unifiedpublish';")
    for table in cursor.fetchall():
        table_names.append(table[0])
    cursor.close()
    return table_names

def get_postgres_column_names(conn2, table_name):
    """Return a list of column names."""
    column_names = []
    cursor2 = conn2.cursor()
    columns_query = cursor2.execute(f"select column_name from information_schema.columns where table_name = '{table_name}';")
    columns = cursor2.fetchall()
    #columns = conn2.execute(f"PRAGMA table_info('{table_name}');").fetchall()
    print(columns)
    for col in columns:
        column_names.append(col[0])
    cursor2.close()
    return column_names


def get_database_info(conn2):
    """Return a list of dicts containing the table name and columns for each table in the database."""
    table_dicts = []
    for table_name in get_postgres_table_names(conn2):
        columns_names = get_postgres_column_names(conn2, table_name)
        table_dicts.append({"table_name": table_name, "column_names": columns_names})
    return table_dicts

def ask_database(conn2, query):
    """Function to query SQLite database with a provided SQL query."""
    try:
        cursor3 = conn2.cursor()
        results_query = str(cursor3.execute(query))
        results = cursor3.fetchall()
    except Exception as e:
        results = f"query failed with error: {e}"
    return results

def execute_function_call(conn2,message):
    if message["tool_calls"][0]["function"]["name"] == "ask_database":
        query = json.loads(message["tool_calls"][0]["function"]["arguments"])["query"]
        results = ask_database(conn2, query)
    else:
        results = f"Error: function {message['tool_calls'][0]['function']['name']} does not exist"
    return results