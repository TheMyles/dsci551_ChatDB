import pymongo
import pymysql
import pandas as pd

from generate_sql_examples_final import get_mysql_metadata
from generate_sql_examples_final import execute_queries

from mongo_examples_testing import get_mongodb_metadata

# login_info = {
#     'endpoint': "localhost",
#     'username': "root",
#     'password': "Bobo8128!",
#     'sql_database_name': "chatdb",
#     'mongo_username': 'mdmolnar',
#     'mongo_password': 'AtM0nG0d1452',
#     'mongo_database_name': "ChatDB",
# }

# connection = pymysql.connect(
#     host=login_info['endpoint'],
#     user=login_info['username'],
#     password=login_info['password'],
#     database=login_info['sql_database_name']
# )

def explore_data(sql_metadata, mongo_metadata, connection, login_info):
    # While loop to keep asking for valid input
    while True:
        # Prompt the user to select MongoDB or SQL
        user_choice = input("Please select the data source to explore (MongoDB/SQL): ").strip().lower()

        # If the user selects SQL
        if user_choice == 'sql':
            explore_sql(sql_metadata, connection)
            break  # Exit the loop once SQL is selected and handled
        
        # If the user selects MongoDB
        elif user_choice == 'mongodb':
            explore_mongodb(mongo_metadata, login_info, connection)
            break  # Exit the loop once MongoDB is selected and handled
        
        # If the user enters an invalid selection
        else:
            print("Invalid choice. Please select 'MongoDB' or 'SQL'.")

        

def explore_sql(metadata, connection):
    try:
        if not metadata:
            print("No tables found in the metadata.")
            return

        cursor = connection.cursor()

        for table_name in metadata.keys():
            print(f"\nDescribing table: {table_name}")

            # Execute the SQL query to describe the table (equivalent of .describe in pandas)
            query = f"DESCRIBE {table_name};"
            cursor.execute(query)

            # Fetch and display the description of the table
            table_description = cursor.fetchall()
            print("Table structure:")
            execute_queries(query, connection)  # Show table structure in a tabular format

            # Now, display the top 5 rows using SELECT * FROM <table_name> LIMIT 5
            print(f"\nSample data (top 5 rows) from {table_name}:")
            select_query = f"SELECT * FROM {table_name} LIMIT 5;"
            execute_queries(select_query, connection)  # Show the top 5 rows of the table

    except pymysql.MySQLError as err:
        print(f"Error while accessing the database: {err}")
    finally:
        cursor.close()


# # Placeholder for MongoDB exploration (you can fill this in with MongoDB-related functionality)
# def explore_mongodb():
#     print("MongoDB exploration functionality will be implemented here.")
#     # You can implement further MongoDB exploration logic here


# Function to explore MongoDB data by showing collections, fields, and sample data
def explore_mongodb(metadata, login_info, connection=None):
    # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']
    database_name = login_info['mongo_database_name']
    connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'
    # Connect to MongoDB
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]

    # Iterate over collections in metadata
    for collection_name in metadata.keys():
        print(f"\nDescribing collection: {collection_name}")

        # Get metadata: fetch a sample document to infer field types
        collection = db[collection_name]
        sample_doc = collection.find_one()  # Fetch one document to inspect its structure

        if sample_doc:
            print("Collection structure (fields and types):")
            for field, value in sample_doc.items():
                print(f"  - {field}: {type(value).__name__}")  # Print field name and its type
        else:
            print("No documents found in this collection.")

        # Display the top 5 rows using SELECT * FROM <collection_name> LIMIT 5 equivalent
        print(f"\nSample data (top 5 rows) from {collection_name}:")
        sample_data = collection.find().limit(5)  # Fetch top 5 documents

        # Convert the result to a list and display in a tabular format using pandas and tabulate
        sample_data_list = list(sample_data)
        if sample_data_list:
            sample_df = pd.DataFrame(sample_data_list)
            print(sample_df.to_markdown(index=False))  # Display the top 5 rows in tabular format (markdown style)
        else:
            print("No sample data available.")


# testing
# sql_metadata = get_mysql_metadata(login_info)
# mongo_metadata = get_mongodb_metadata(login_info)

# explore_data(sql_metadata, mongo_metadata, connection)