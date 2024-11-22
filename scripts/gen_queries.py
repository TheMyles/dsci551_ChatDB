import pymysql
import pymongo

# import mysql.connector

from decimal import Decimal

def get_mysql_metadata(connection, database_name):
    metadata = {}
    cursor = connection.cursor()
    cursor.execute(f"USE {database_name}")
    
    # Get all table names
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        print("=" * 20)  # Separator line
        print(f"Table: {table}")
        
        # Get column names and types
        cursor.execute(f"DESCRIBE {table}")
        columns = [{"name": row[0], "type": row[1], "unique_values": []} for row in cursor.fetchall()]
        
        # Fetch unique values for each column
        for column in columns:
            column_name = column["name"]
            cursor.execute(f"SELECT DISTINCT `{column_name}` FROM `{table}` LIMIT 5")  # Limit for performance
            unique_values = [row[0] for row in cursor.fetchall()]
            
            # Convert Decimal to float if applicable
            unique_values = [
                float(value) if isinstance(value, Decimal) else value
                for value in unique_values
            ]
            
            column["unique_values"] = unique_values
        
        metadata[table] = columns  # Store metadata for the table
        
        # Print metadata for debugging
        for column in columns:
            print(f"Column: {column['name']}, Type: {column['type']}, Unique Values: {column['unique_values']}")
    
    return metadata



# Example usage
endpoint = "localhost"
username = "root"
passwordjacob = "Bobo8128!"
database_name = "chatdb"

connection = pymysql.connect(
    host=endpoint,
    user=username,
    password=passwordjacob,
    database=database_name
)

metadata = get_mysql_metadata(connection, "chatdb")
print("="* 100)
print(metadata['generalinfo'])

# print("\nMetadata:")
# print(metadata)

# metadata = get_mysql_metadata(connection, "chatdb")
# metadata, table_names, column_names = get_mysql_metadata(connection, "chatdb")

# print("\nTables:")
# print(table_names)
# print("\nColumns:")
# print(column_names)


# import random

# def generate_sql_query(template, metadata):
#     # Pick a random table
#     table_name = random.choice(list(metadata.keys()))
#     columns = metadata[table_name]
    
#     query = template.replace("<TABLE>", table_name)
    
#     if "<COLUMN>" in template:
#         column = random.choice(columns)  # Choose a random column from the selected table
#         query = query.replace("<COLUMN>", column)
    
#     if "<VALUE>" in template:
#         value = "100"  # Example value (can be customized)
#         query = query.replace("<VALUE>", value)
    
#     return query

# # Example usage
# sql_template = "SELECT <COLUMN> FROM <TABLE> WHERE <COLUMN> > <VALUE>;"
# query = generate_sql_query(sql_template, metadata)
# print("\nGenerated Query:")
# print(query)

import random


def generate_sql_query(metadata):
    # List of query templates
    templates = [
        "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> = <NUMVALUE>;",
        "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> > <NUMVALUE>;",
        "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> < <NUMVALUE>;",
        "SELECT DISTINCT <COLUMN> FROM <TABLE>;",
        "SELECT COUNT(<COLUMN>) FROM <TABLE>;",
        "SELECT AVG(<NUMCOLUMN>) FROM <TABLE>;",
        "SELECT SUM(<NUMCOLUMN>) FROM <TABLE>;",
        "SELECT MIN(<NUMCOLUMN>) FROM <TABLE>;",
        "SELECT MAX(<NUMCOLUMN>) FROM <TABLE>;",
        "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE> WHERE <COLUMN1> = <STRVALUE>;",
        "SELECT * FROM <TABLE> WHERE <COLUMN> LIKE '%<STRVALUE>%';",
        "SELECT <COLUMN> FROM <TABLE> ORDER BY <COLUMN> ASC;",
        "SELECT <COLUMN> FROM <TABLE> ORDER BY <COLUMN> DESC;",
        "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> BETWEEN <NUMVALUE> AND <NUMVALUE>;",
        "SELECT <COLUMN1>, COUNT(<COLUMN2>) FROM <TABLE> GROUP BY <COLUMN1>;",
        "SELECT <COLUMN1>, SUM(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN1>;",
        "SELECT <COLUMN1>, AVG(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN1>;",
        "SELECT * FROM <TABLE> WHERE <COLUMN> IN (<STRVALUE>, <STRVALUE>, <STRVALUE>);",
        "SELECT <COLUMN> FROM <TABLE> LIMIT <NUMVALUE>;",
        "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE> WHERE <COLUMN1> = <STRVALUE> AND <NUMCOLUMN> < <NUMVALUE>;"
    ]
    
    # Pick a random template
    template = random.choice(templates)
    
    # Pick a random table
    table_name = random.choice(list(metadata.keys()))
    columns = metadata[table_name]  # Get column metadata for the table
    
    query = template.replace("<TABLE>", table_name)
    
    # Replace <NUMCOLUMN> placeholders
    while "<NUMCOLUMN>" in query:
        num_column = random.choice([col for col in columns if col["type"] in ("int", "float", "decimal")])
        query = query.replace("<NUMCOLUMN>", num_column["name"], 1)
    
    # Replace <COLUMN> placeholders
    while "<COLUMN>" in query:
        column = random.choice(columns)
        query = query.replace("<COLUMN>", column["name"], 1)
    
    # Replace <COLUMN1> and <COLUMN2> placeholders
    while "<COLUMN1>" in query:
        column1 = random.choice(columns)
        query = query.replace("<COLUMN1>", column1["name"], 1)
    while "<COLUMN2>" in query:
        column2 = random.choice(columns)
        query = query.replace("<COLUMN2>", column2["name"], 1)
    
    # Replace <NUMVALUE> placeholders
    while "<NUMVALUE>" in query:
        num_column = random.choice([col for col in columns if col["type"] in ("int", "float", "decimal")])
        if num_column["unique_values"]:
            num_value = random.choice(num_column["unique_values"])
        else:
            num_value = 0  # Default value if no unique values
        query = query.replace("<NUMVALUE>", str(num_value), 1)
    
    # Replace <STRVALUE> placeholders
    while "<STRVALUE>" in query:
        str_column = random.choice([col for col in columns if "char" in col["type"] or "text" in col["type"]])
        if str_column["unique_values"]:
            str_value = random.choice(str_column["unique_values"])
            str_value = f"'{str_value}'"  # Add quotes for string values
        else:
            str_value = "'default'"  # Default string value
        query = query.replace("<STRVALUE>", str_value, 1)
    
    # Replace generic <VALUE> placeholders (if applicable)
    while "<VALUE>" in query:
        column = random.choice(columns)
        if column["unique_values"]:
            value = random.choice(column["unique_values"])
            if isinstance(value, str):
                value = f"'{value}'"  # Add quotes for string values
        else:
            value = "NULL"
        query = query.replace("<VALUE>", str(value), 1)
    
    return query

# Generate and print 5 queries at a time
for _ in range(5):
    query = generate_sql_query(metadata)
    print("\nGenerated Query:")
    print(query)


'''
values must be selected from the associated column
choosing from an empty sequence happens when geographic is selected (pronbably)
dont allow to do numerical stuff by primary key

'''