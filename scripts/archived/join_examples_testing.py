import random
import pymysql
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
        print("=" * 20)  # Separator line
        print(f"Table: {table}")
        
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
            print(f"Column: {column['name']}, Type: {column['type']}, Primary Key: {column['primary_key']}, Unique Values: {column['unique_values']}")
    
    connection.close()  # Close the connection after use
    return metadata


login_info = {
    'endpoint': "localhost",
    'username': "root",
    'password': "Bobo8128!",
    'database_name': "chatdb",
    'mongo_username': 'mdmolnar',
    'mongo_password': 'AtM0nG0d1452'
}

metadata = get_mysql_metadata(login_info)

# def generate_sql_query(metadata, connection):
#     # Query templates grouped by type with summary placeholders
#     templates_with_summaries = [
#         {
#             "query": "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2>;",
#             "summary": "Find rows by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>, showing <COLUMN1> and <COLUMN2>."
#         },
#         {
#             "query": "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2> WHERE <TABLE1>.<COLUMN1> = <STRVALUE>;",
#             "summary": "Find rows from <TABLE1> and <TABLE2> where <COLUMN1> equals <STRVALUE>, joining on <JOINT_COLUMN1> and <JOINT_COLUMN2>, showing <COLUMN1> and <COLUMN2>."
#         },
#         {
#             "query": "SELECT COUNT(*) FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2>;",
#             "summary": "Count rows by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
#         },
#         {
#             "query": "SELECT <COLUMN> FROM <TABLE> WHERE <COLUMN> = <STRVALUE>;",
#             "summary": "Find rows from <TABLE> where <COLUMN> equals <STRVALUE>."
#         },
#         # Add more templates here as needed
#     ]
    
#     # Pick random tables for JOIN queries
#     table1, table2 = random.sample(list(metadata.keys()), 2)  # Randomly pick two tables
#     columns_table1 = metadata[table1]
#     columns_table2 = metadata[table2]
    
#     # Determine joinable columns (primary keys and naming conventions)
#     joinable_columns_table1 = [
#         col for col in columns_table1 if col["primary_key"] or "id" in col["name"] or "key" in col["name"]
#     ]
#     joinable_columns_table2 = [
#         col for col in columns_table2 if col["primary_key"] or "id" in col["name"] or "key" in col["name"]
#     ]
    
#     if joinable_columns_table1 and joinable_columns_table2:
#         joint_column1 = random.choice(joinable_columns_table1)
#         joint_column2 = random.choice(joinable_columns_table2)
#     else:
#         joint_column1, joint_column2 = None, None  # No joinable columns found
    
#     # Pick a random template
#     template_data = random.choice(templates_with_summaries)
#     query = template_data["query"]
#     summary = template_data["summary"]
    
#     # Replace table placeholders
#     query = query.replace("<TABLE1>", table1).replace("<TABLE2>", table2)
#     summary = summary.replace("<TABLE1>", table1).replace("<TABLE2>", table2)
    
#     # Replace joint column placeholders if applicable
#     if joint_column1 and joint_column2:
#         query = query.replace("<JOINT_COLUMN1>", joint_column1["name"])
#         query = query.replace("<JOINT_COLUMN2>", joint_column2["name"])
#         summary = summary.replace("<JOINT_COLUMN1>", joint_column1["name"])
#         summary = summary.replace("<JOINT_COLUMN2>", joint_column2["name"])
    
#     # Handle column replacements
#     columns_table1_names = [col["name"] for col in columns_table1]
#     columns_table2_names = [col["name"] for col in columns_table2]
    
#     while "<COLUMN1>" in query:
#         column1 = random.choice(columns_table1_names)
#         query = query.replace("<COLUMN1>", column1, 1)
#         summary = summary.replace("<COLUMN1>", column1, 1)
    
#     while "<COLUMN2>" in query:
#         column2 = random.choice(columns_table2_names)
#         query = query.replace("<COLUMN2>", column2, 1)
#         summary = summary.replace("<COLUMN2>", column2, 1)
    
#     # Replace <STRVALUE> with unique values from the associated column
#     while "<STRVALUE>" in query:
#         str_column = random.choice([col for col in columns_table1 if "char" in col["type"] or "text" in col["type"]])
#         if str_column["unique_values"]:
#             str_value = random.choice(str_column["unique_values"])
#         else:
#             str_value = "default"
#         str_value = str(str_value)  # Ensure it's a string
#         query = query.replace("<STRVALUE>", f"'{str_value}'", 1)
#         summary = summary.replace("<STRVALUE>", str_value, 1)
    
#     return query, summary


def generate_sql_query(metadata, connection):
    # Query templates grouped by type with summary placeholders
    templates_with_summaries = [
        {
            "query": "SELECT <COLUMN1>, <COLUMN2> FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2>;",
            "summary": "Find rows by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>, showing <COLUMN1> and <COLUMN2>."
        },
        {
            "query": "SELECT AVG(<NUMCOLUMN>) FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2> WHERE <TABLE1>.<COLUMN1> = <STRVALUE>;",
            "summary": "Find the average of <NUMCOLUMN> from <TABLE1> and <TABLE2>, filtered where <COLUMN1> equals <STRVALUE>, joining on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
        },
        {
            "query": "SELECT <COLUMN1>, SUM(<NUMCOLUMN>) FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2> GROUP BY <COLUMN1>;",
            "summary": "Find the sum of <NUMCOLUMN> grouped by <COLUMN1> by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
        },
        {
            "query": "SELECT <COLUMN1>, MAX(<NUMCOLUMN>) FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2> WHERE <COLUMN2> LIKE '%<STRVALUE>%' GROUP BY <COLUMN1>;",
            "summary": "Find the maximum of <NUMCOLUMN>, grouped by <COLUMN1> where <COLUMN2> contains <STRVALUE>, joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
        },
        {
            "query": "SELECT COUNT(*) FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2>;",
            "summary": "Count rows by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
        },
        {
            "query": "SELECT DISTINCT <COLUMN1>, <COLUMN2> FROM <TABLE1> INNER JOIN <TABLE2> ON <TABLE1>.<JOINT_COLUMN1> = <TABLE2>.<JOINT_COLUMN2> WHERE <COLUMN2> = <STRVALUE>;",
            "summary": "Find distinct rows for <COLUMN1> and <COLUMN2> where <COLUMN2> equals <STRVALUE>, by joining <TABLE1> and <TABLE2> on <JOINT_COLUMN1> and <JOINT_COLUMN2>."
        }
    ]
    
    # Pick random tables for JOIN queries
    table1, table2 = random.sample(list(metadata.keys()), 2)  # Randomly pick two tables
    columns_table1 = metadata[table1]
    columns_table2 = metadata[table2]
    
    # Determine joinable columns (primary keys and naming conventions)
    joinable_columns_table1 = [
        col for col in columns_table1 if col["primary_key"] or "id" in col["name"] or "key" in col["name"]
    ]
    joinable_columns_table2 = [
        col for col in columns_table2 if col["primary_key"] or "id" in col["name"] or "key" in col["name"]
    ]
    
    if joinable_columns_table1 and joinable_columns_table2:
        joint_column1 = random.choice(joinable_columns_table1)
        joint_column2 = random.choice(joinable_columns_table2)
    else:
        joint_column1, joint_column2 = None, None  # No joinable columns found
    
    # Pick a random template
    template_data = random.choice(templates_with_summaries)
    query = template_data["query"]
    summary = template_data["summary"]
    
    # Replace table placeholders
    query = query.replace("<TABLE1>", table1).replace("<TABLE2>", table2)
    summary = summary.replace("<TABLE1>", table1).replace("<TABLE2>", table2)
    
    # Replace joint column placeholders if applicable
    if joint_column1 and joint_column2:
        query = query.replace("<JOINT_COLUMN1>", joint_column1["name"])
        query = query.replace("<JOINT_COLUMN2>", joint_column2["name"])
        summary = summary.replace("<JOINT_COLUMN1>", joint_column1["name"])
        summary = summary.replace("<JOINT_COLUMN2>", joint_column2["name"])
    
    # Handle column replacements
    columns_table1_names = [col["name"] for col in columns_table1]
    columns_table2_names = [col["name"] for col in columns_table2]
    
    while "<COLUMN1>" in query:
        column1 = random.choice(columns_table1_names)
        query = query.replace("<COLUMN1>", column1, 1)
        summary = summary.replace("<COLUMN1>", column1, 1)
    
    while "<COLUMN2>" in query:
        column2 = random.choice(columns_table2_names)
        query = query.replace("<COLUMN2>", column2, 1)
        summary = summary.replace("<COLUMN2>", column2, 1)
    
    # Replace <NUMCOLUMN> placeholders, excluding primary keys
    while "<NUMCOLUMN>" in query:
        numeric_columns = [
            col["name"] for col in columns_table1 if col["type"] in ("int", "float", "decimal") and not col["primary_key"]
        ]
        if not numeric_columns:
            return "Error: No numeric columns available for the selected table.", None
        num_column = random.choice(numeric_columns)
        query = query.replace("<NUMCOLUMN>", num_column, 1)
        summary = summary.replace("<NUMCOLUMN>", num_column, 1)
    
    # Replace <NUMVALUE> placeholders with random numeric values
    while "<NUMVALUE>" in query:
        num_value = random.randint(1, 100)  # Replace with random numeric value
        query = query.replace("<NUMVALUE>", str(num_value), 1)
        summary = summary.replace("<NUMVALUE>", str(num_value), 1)
    
    # Replace <STRVALUE> with unique values from the associated column
    while "<STRVALUE>" in query:
        str_column = random.choice([col for col in columns_table1 if "char" in col["type"] or "text" in col["type"]])
        if str_column["unique_values"]:
            str_value = random.choice(str_column["unique_values"])
        else:
            str_value = "default"
        str_value = str(str_value)  # Ensure it's a string
        query = query.replace("<STRVALUE>", f"'{str_value}'", 1)
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


connection = pymysql.connect(
    host='localhost',
    user='root',
    password="Bobo8128!",
    database="chatdb"
)

# Generate and print 5 queries at a time
for _ in range(5):
    while True:
        sql_query, summary_text = generate_sql_query(metadata, connection)
        if sql_query.startswith("Error:") or not validate_query(sql_query, connection):
            continue  # Retry if the query is invalid or fails
        print("\nGenerated Query:")
        print(sql_query)
        print("Summary:")
        print(summary_text)
        break
