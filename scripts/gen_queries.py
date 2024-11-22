import pymysql
import pymongo

# import mysql.connector

def get_mysql_metadata(login_info):
    metadata = {}  # Dictionary to store table and column names

    connection = pymysql.connect(
        host=login_info['endpoint'],
        user=login_info['username'],
        password=login_info['password'],
        db=login_info['database_name']
    )

    cursor = connection.cursor()
    
    # Get all table names
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        # print("=" * 20)  # Separator line
        # print(f"Table: {table}")
        
        cursor.execute(f"DESCRIBE {table}")
        columns = [row[0] for row in cursor.fetchall()]  # Extract column names only
        metadata[table] = columns  # Store columns under the respective table
        
        # for column in columns:
        #     print(f"Column: {column}")
    
    connection.close()
    
    return metadata

# Example usage

login_info = {
    'endpoint': "localhost",
    'username': "root",
    'password': "MySQLDBP455",
    'database_name': "chatdb",
    'mongo_username': 'mdmolnar',
    'mongo_password': 'AtM0nG0d1452'
}

endpoint = "localhost"
username = "root"
passwordjacob = "MySQLDBP455"
database_name = "chatdb"

connection = pymysql.connect(
    host=login_info['endpoint'],
    user=login_info['username'],
    password=login_info['password'],
    db=login_info['database_name']
)

metadata = get_mysql_metadata(login_info)
print("\nMetadata:")
print(metadata)

# metadata = get_mysql_metadata(connection, "chatdb")
# metadata, table_names, column_names = get_mysql_metadata(connection, "chatdb")

# print("\nTables:")
# print(table_names)
# print("\nColumns:")
# print(column_names)


import random

def generate_sql_query(template, metadata):
    # Pick a random table
    table_name = random.choice(list(metadata.keys()))
    columns = metadata[table_name]
    
    query = template.replace("<TABLE>", table_name)
    
    if "<COLUMN>" in template:
        column = random.choice(columns)  # Choose a random column from the selected table
        query = query.replace("<COLUMN>", column)
    
    if "<VALUE>" in template:
        value = "100"  # Example value (can be customized)
        query = query.replace("<VALUE>", value)
    
    return query

# Example usage
sql_template = "SELECT <COLUMN> FROM <TABLE> WHERE <COLUMN> > <VALUE>;"
query = generate_sql_query(sql_template, metadata)
print("\nGenerated Query:")
print(query)

