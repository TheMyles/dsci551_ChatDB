import pymongo
import pymysql
import pandas as pd

def nosql_upload(keywords, user_input):



    return



def sql_upload(user_input):

    endpoint = "localhost"
    username = "root"
    password = "MySQLDBP455"
    database_name = "chatdb"
    port = 3306 

    connection = pymysql.connect(
        host=endpoint,
        user=username,
        password=password,
        database=database_name
    )

    for i in user_input.split():
        if '/' in i or '\\' in i:
            file_path = i
    
    table_name = file_path.split('/')[-1][:-4]

    print(file_path)
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

            print(create_query)

            cursor.execute(create_query)

            column_names = ', '.join(sql_df.columns)  # Join column names as a string
            placeholders = ', '.join(['%s'] * len(sql_df.columns))  # Placeholder for each column value
            
            insert_query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
            
            # Loop over each row in the DataFrame and execute the query
            for _, row in sql_df.iterrows():
                values = tuple(row)  # Convert the row to a tuple
                print(insert_query, values)  # Debug: print query and values
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