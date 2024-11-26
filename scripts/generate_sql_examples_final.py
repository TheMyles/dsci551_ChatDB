import pymysql
import pymongo
from decimal import Decimal

def get_mysql_metadata(login_info):
    metadata = {}

    # Connect to the MySQL database
    connection = pymysql.connect(
        host=login_info['endpoint'],
        user=login_info['username'],
        password=login_info['password'],
        database=login_info['database_name']
    )

    cursor = connection.cursor()
    
    # Get all table names
    cursor.execute("SHOW TABLES")
    tables = [table[0] for table in cursor.fetchall()]
    
    for table in tables:
        # print("=" * 20)  # Separator line
        # print(f"Table: {table}")
        
        # Get column metadata
        cursor.execute(f"DESCRIBE {table}")
        columns = [{"name": row[0], "type": row[1], "primary_key": False, "unique_values": []} for row in cursor.fetchall()]
        
        # Identify primary keys
        cursor.execute(f"SHOW KEYS FROM {table} WHERE Key_name = 'PRIMARY'")
        primary_keys = {row[4] for row in cursor.fetchall()}  # Column names of primary keys
        for column in columns:
            if column["name"] in primary_keys:
                column["primary_key"] = True
        
        # Fetch unique values for each column
        for column in columns:
            column_name = column["name"]
            cursor.execute(f"SELECT DISTINCT `{column_name}` FROM `{table}`")  # Limit for performance
            unique_values = [row[0] for row in cursor.fetchall()]
            
            # Convert Decimal to float if applicable
            unique_values = [
                float(value) if isinstance(value, Decimal) else value
                for value in unique_values
            ]
            
            column["unique_values"] = unique_values
        
        metadata[table] = columns  # Store metadata for the table
        
        # # Print metadata for debugging
        # for column in columns:
        #     print(f"Column: {column['name']}, Type: {column['type']}, Primary Key: {column['primary_key']}, Unique Values: {column['unique_values']}")
    
    connection.close()  # Close the connection after use
    return metadata


# login_info = {
#     'endpoint': "localhost",
#     'username': "root",
#     'password': "Bobo8128!",
#     'database_name': "chatdb",
#     'mongo_username': 'mdmolnar',
#     'mongo_password': 'AtM0nG0d1452'
# }

# metadata = get_mysql_metadata(login_info)

import random
import pymysql

def generate_sql_query(metadata, connection):
    # Query templates grouped by type with summary placeholders
    templates_with_summaries = [
        # Existing templates
        {
            "query": "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> = <NUMVALUE>;",
            "summary": "Find rows from <TABLE> where <NUMCOLUMN> equals <NUMVALUE>."
        },
        {
            "query": "SELECT <NUMCOLUMN> FROM <TABLE> WHERE <NUMCOLUMN> > <NUMVALUE>;",
            "summary": "Find rows from <TABLE> where <NUMCOLUMN> is greater than <NUMVALUE>."
        },
        {
            "query": "SELECT AVG(<NUMCOLUMN>) FROM <TABLE>;",
            "summary": "Find the average value of <NUMCOLUMN> from <TABLE>."
        },
        {
            "query": "SELECT DISTINCT <COLUMN> FROM <TABLE>;",
            "summary": "Find distinct values of <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT COUNT(<COLUMN>) FROM <TABLE>;",
            "summary": "Count the number of rows for <COLUMN> in <TABLE>."
        },
        {
            "query": "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE> WHERE <COLUMN1> = <STRVALUE>;",
            "summary": "Find rows from <TABLE> where <COLUMN1> equals <STRVALUE>, showing <COLUMN1> and <COLUMN2>."
        },
        {
            "query": "SELECT * FROM <TABLE> WHERE <COLUMN> LIKE '%<STRVALUE>%';",
            "summary": "Find rows from <TABLE> where <COLUMN> contains '<STRVALUE>'."
        },
        {
            "query": "SELECT * FROM <TABLE> WHERE <COLUMN> IN (<STRVALUE>, <STRVALUE>, <STRVALUE>);",
            "summary": "Find rows from <TABLE> where <COLUMN> matches one of the given values."
        },
        {
            "query": "SELECT <COLUMN> FROM <TABLE> ORDER BY <COLUMN> ASC;",
            "summary": "Show <COLUMN> details from <TABLE>, sorted in ascending order."
        },
        {
            "query": "SELECT <COLUMN> FROM <TABLE> ORDER BY <COLUMN> DESC;",
            "summary": "Show <COLUMN> details from <TABLE>, sorted in descending order."
        },
        {
            "query": "SELECT <COLUMN> FROM <TABLE> LIMIT <NUMVALUE>;",
            "summary": "Show <COLUMN> details from <TABLE>, limited to <NUMVALUE> rows."
        },

        # New complex templates
        {
            "query": "SELECT <COLUMN>, COUNT(*) FROM <TABLE> GROUP BY <COLUMN>;",
            "summary": "Count the number of rows grouped by <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, SUM(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN>;",
            "summary": "Find the sum of <NUMCOLUMN> grouped by <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, AVG(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN>;",
            "summary": "Find the average value of <NUMCOLUMN> grouped by <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, MAX(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN>;",
            "summary": "Find the maximum value of <NUMCOLUMN> grouped by <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, MIN(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN>;",
            "summary": "Find the minimum value of <NUMCOLUMN> grouped by <COLUMN> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, COUNT(*) FROM <TABLE> GROUP BY <COLUMN> HAVING COUNT(*) > <NUMVALUE>;",
            "summary": "Find groups of <COLUMN> where the count of rows is greater than <NUMVALUE> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, AVG(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN> HAVING AVG(<NUMCOLUMN>) > <NUMVALUE>;",
            "summary": "Find groups of <COLUMN> where the average value of <NUMCOLUMN> is greater than <NUMVALUE> from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, SUM(<NUMCOLUMN>) FROM <TABLE> WHERE <COLUMN> LIKE '%<STRVALUE>%' GROUP BY <COLUMN>;",
            "summary": "Find the sum of <NUMCOLUMN> grouped by <COLUMN>, where <COLUMN> contains '<STRVALUE>', from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, MAX(<NUMCOLUMN>) FROM <TABLE> WHERE <COLUMN> IN (<STRVALUE>, <STRVALUE>, <STRVALUE>) GROUP BY <COLUMN>;",
            "summary": "Find the maximum value of <NUMCOLUMN> grouped by <COLUMN>, where <COLUMN> matches one of the given values, from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, COUNT(*) FROM <TABLE> WHERE <COLUMN> = <STRVALUE> GROUP BY <COLUMN> ORDER BY COUNT(*) DESC;",
            "summary": "Count rows grouped by <COLUMN>, filtered by <STRVALUE>, and sorted by the count in descending order from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, COUNT(*) FROM <TABLE> WHERE <NUMCOLUMN> BETWEEN <NUMVALUE> AND <NUMVALUE> GROUP BY <COLUMN>;",
            "summary": "Count rows grouped by <COLUMN>, where <NUMCOLUMN> falls between <NUMVALUE> and <NUMVALUE>, from <TABLE>."
        },
        {
            "query": "SELECT <COLUMN>, SUM(<NUMCOLUMN>) FROM <TABLE> GROUP BY <COLUMN> HAVING SUM(<NUMCOLUMN>) > <NUMVALUE>;",
            "summary": "Find groups of <COLUMN> where the sum of <NUMCOLUMN> is greater than <NUMVALUE> from <TABLE>."
        }
    ]

    
    # Pick a random table
    table_name = random.choice(list(metadata.keys()))
    columns = metadata[table_name]  # Get column metadata for the table
    
    # Check if the table has numeric columns (excluding primary keys)
    numeric_columns = [col for col in columns if col["type"] in ("int", "float", "decimal") and not col["primary_key"]]
    has_numeric = bool(numeric_columns)
    if has_numeric:
        templates = templates_with_summaries
    else:
        templates = [t for t in templates_with_summaries if "<NUMCOLUMN>" not in t["query"]]
    
    # Pick a random template
    template_data = random.choice(templates)
    query = template_data["query"].replace("<TABLE>", table_name)
    summary = template_data["summary"].replace("<TABLE>", table_name)
    
    # Initialize placeholders
    last_used_column = None
    last_used_column1 = None  # For <COLUMN1>
    
    # Replace <NUMCOLUMN> placeholders
    while "<NUMCOLUMN>" in query:
        if not numeric_columns:
            return "Error: No valid numeric columns available in the selected table.", None
        num_column = random.choice(numeric_columns)
        query = query.replace("<NUMCOLUMN>", num_column["name"])
        summary = summary.replace("<NUMCOLUMN>", num_column["name"])
        last_used_column = num_column  # Track the column for <NUMVALUE>
    
    # Replace <NUMVALUE> placeholders using the last used numeric column
    while "<NUMVALUE>" in query:
        if last_used_column and last_used_column["unique_values"]:
            num_value = random.choice(last_used_column["unique_values"])
        else:
            return "Error: No valid numeric values available for the selected column.", None
        query = query.replace("<NUMVALUE>", str(num_value))
        summary = summary.replace("<NUMVALUE>", str(num_value))
    
    # Replace <COLUMN1> and <COLUMN2> placeholders (ensure distinct columns)
    while "<COLUMN1>" in query:
        column1 = random.choice(columns)
        query = query.replace("<COLUMN1>", column1["name"])
        summary = summary.replace("<COLUMN1>", column1["name"])
        last_used_column1 = column1  # Track the column for <STRVALUE>
    while "<COLUMN2>" in query:
        column2 = random.choice([col for col in columns if col != last_used_column1])
        query = query.replace("<COLUMN2>", column2["name"])
        summary = summary.replace("<COLUMN2>", column2["name"])
    
    # Replace <COLUMN> placeholders
    while "<COLUMN>" in query:
        column = random.choice(columns)
        query = query.replace("<COLUMN>", column["name"])
        summary = summary.replace("<COLUMN>", column["name"])
    
    # Replace <STRVALUE> placeholders one at a time
    while "<STRVALUE>" in query:
        str_columns = [col for col in columns if "char" in col["type"] or "text" in col["type"]]
        if not str_columns:
            return "Error: No valid string columns available in the selected table.", None
        str_column = random.choice(str_columns)
        if str_column["unique_values"]:
            str_value = random.choice(str_column["unique_values"])
        else:
            str_value = "default"
        str_value = str(str_value)  # Ensure str_value is always a string
        if "LIKE" in query and "%<STRVALUE>%" in query:
            query = query.replace("%<STRVALUE>%", f"%{str_value}%", 1)  # Replace only one instance
            summary = summary.replace("<STRVALUE>", str_value, 1)
        else:
            query = query.replace("<STRVALUE>", f"'{str_value}'", 1)  # Replace only one instance
            summary = summary.replace("<STRVALUE>", str_value, 1)
    
    return query, summary


# Function to validate query execution in MySQL
def validate_query(query, connection):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return bool(results)  # Return True if results exist, False otherwise
    except pymysql.Error:
        return False