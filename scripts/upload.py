import pymongo
import pymysql
import pandas as pd
import json
from bson import ObjectId

def mongo_upload(user_input, login_info):
    # Extract file path from user input
    file_path = None
    for i in user_input.split():
        if '/' in i or '\\' in i:
            file_path = i
            break

    if not file_path:
        print("No valid file path found in input.")
        return

    # Extract table name from file path
    table_name = file_path.split('/')[-1].split('.')[0]

    # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']

    connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string)
        db = client["ChatDB"]

        # Check if the collection exists
        if table_name not in db.list_collection_names():
            print(f"Creating collection '{table_name}'...")
        else:
            print(f"Using existing collection '{table_name}'.")

        # Access the collection
        collection = db[table_name]

        # Load the JSON file
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Ensure data is in the correct format (list of documents)
            if isinstance(data, dict):
                data = [data]

            data = [convert_extended_json(doc) for doc in data]

            # Insert data into the collection
            result = collection.insert_many(data)
            print(f"Inserted {len(result.inserted_ids)} documents into collection '{table_name}'.")
        except FileNotFoundError:
            print("The specified JSON file does not exist.")
        except json.JSONDecodeError:
            print("Failed to decode the JSON file. Ensure it is correctly formatted.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
    except pymongo.errors.ConnectionError:
        print("Failed to connect to MongoDB. Please check your connection string and credentials.")
    finally:
        # Close the connection
        client.close()

    return

def convert_extended_json(doc):
    for key, value in doc.items():
        if isinstance(value, dict):
            if "$oid" in value:
                doc[key] = ObjectId(value["$oid"])
            else:
                # Recursively process nested dictionaries
                doc[key] = convert_extended_json(value)
        elif isinstance(value, list):
            # Recursively process lists
            doc[key] = [convert_extended_json(item) if isinstance(item, dict) else item for item in value]
    return doc

def sql_upload(user_input, login_info):

    for i in user_input.split():
        if '/' in i or '\\' in i:
            file_path = i
            break
    
    extension = file_path.split('/')[-1].split('.')[1]

    if extension == 'csv':
        sql_csv_upload(user_input, login_info)
    else:
        execute_sql_file(user_input, login_info)

    return


def sql_csv_upload(user_input, login_info):

    endpoint = login_info['endpoint']
    username = login_info['username']
    password = login_info['password']
    database_name = login_info['database_name']
    port = 3306 

    connection = pymysql.connect(
        host=endpoint,
        user=username,
        password=password,
        database=database_name
    )

    file_path = None
    for i in user_input.split():
        if '/' in i or '\\' in i:
            file_path = i
            break
    
    table_name = file_path.split('/')[-1].split('.')[0]

    sql_df = pd.read_csv(file_path)

    try:
        with connection.cursor() as cursor:
            # Ensure the table exists

            create_query = f'CREATE TABLE IF NOT EXISTS {table_name} ('
            pk_exists = False

            for col in sql_df.columns:
                dtype = python_to_sql_type(sql_df[col])

                if col == sql_df.columns[-1]:
                    create_query = create_query + f'{col} {dtype});'
                elif len(sql_df[col].unique()) == sql_df.shape[0] and not pk_exists:
                    create_query = create_query + f'{col} {dtype} PRIMARY KEY, '
                    pk_exists = True
                else:
                    create_query = create_query + f'{col} {dtype}, '


            cursor.execute(create_query)

            column_names = ', '.join(sql_df.columns)  # Join column names as a string
            placeholders = ', '.join(['%s'] * len(sql_df.columns))  # Placeholder for each column value
            
            insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            
            # Loop over each row in the DataFrame and execute the query
            for _, row in sql_df.iterrows():
                values = tuple(row)  # Convert the row to a tuple
                # print(insert_query, values)  # Debug: print query and values
                cursor.execute(insert_query, values)  # Execute query with values

            connection.commit()
    except pymysql.IntegrityError as e:
        print(f"Integrity Error: {e}")
    finally:
        connection.close()


    return


def python_to_sql_type(dtype):
    """Map pandas data types to SQL data types."""
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    elif pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    elif pd.api.types.is_bool_dtype(dtype):
        return 'BOOLEAN'
    elif pd.api.types.is_object_dtype(dtype):
        return 'VARCHAR(255)'  # For string columns
    elif pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    else:
        return 'VARCHAR(255)'  # Default fallback type
    

def execute_sql_file(user_input, login_info):

    endpoint = login_info['endpoint']
    username = login_info['username']
    password = login_info['password']
    database_name = login_info['database_name']

    file_path = None
    for i in user_input.split():
        if '/' in i or '\\' in i:
            file_path = i
            break
    
    try:
        # Connect to the MySQL server
        connection = pymysql.connect(
            host=endpoint,
            user=username,
            password=password,
            database=database_name
        )


        with connection.cursor() as cursor:
            # Read the SQL file
            with open(file_path, 'r') as sql_file:
                sql_commands = sql_file.read()

            # Split SQL commands by semicolon
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:  # Ignore empty commands
                    cursor.execute(command)

        # Commit changes
        connection.commit()
        print("All SQL commands executed successfully.")

    except pymysql.MySQLError as e:
        print(f"Error while connecting to MySQL: {e}")
    except FileNotFoundError:
        print("SQL file not found. Please check the file path.")
    finally:
        if connection:
            connection.close()

