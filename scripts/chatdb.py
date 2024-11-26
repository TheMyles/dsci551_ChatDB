import pymysql
import pymongo
import sys
from input_process import match_query_pattern
from upload import sql_upload, mongo_upload
import gen_queries

from generate_sql_examples_final import get_mysql_metadata
from generate_sql_examples_final import generate_sql_query
from generate_sql_examples_final import validate_query
from generate_sql_examples_final import find_keywords_for_examples
from generate_sql_examples_final import display_queries
from generate_sql_examples_final import execute_queries
from generate_sql_examples_final import display_join_queries

from generate_mongo_examples_final import get_mongodb_metadata
from generate_mongo_examples_final import generate_mongodb_query
from generate_mongo_examples_final import validate_mongo_query
from generate_mongo_examples_final import find_keywords_for_examples_mongo
from generate_mongo_examples_final import display_mongo_queries
from generate_mongo_examples_final import execute_mongo_query

from data_exploration import explore_data

import tabulate
from tabulate import tabulate

"""
Setup MySQL DB
main py file
Functions in secondary py files
    NLP
    [Uploading
    Generating Example queries
    Generating queries] * 2 
"""

login_info = {
    'endpoint': "localhost",
    'username': "root",
    'password': "MySQLDBP455",
    'sql_database_name': "chatdb",
    'mongo_username': 'mdmolnar',
    'mongo_password': 'AtM0nG0d1452',
    'mongo_database_name': "ChatDB",
}

# login_info = {
#     'endpoint': "localhost",
#     'username': "root",
#     'password': "Bobo8128!",
#     'sql_database_name': "chatdb",
#     'mongo_username': 'mdmolnar',
#     'mongo_password': 'AtM0nG0d1452',
#     'mongo_database_name': "ChatDB",
# }

connection = pymysql.connect(
    host=login_info['endpoint'],
    user=login_info['username'],
    password=login_info['password'],
    database=login_info['sql_database_name']
)

# mongo_username = login_info['mongo_username']
# mongo_password = login_info['mongo_password']
# database_name = login_info['mongo_database_name']
# connection_string = f"mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/"
# client = pymongo.MongoClient(connection_string)
# db = client[database_name]

memory = []

def chatdb():
    continue_running = True
    print("Hello! Welcome to ChatDB.")
    print("Would you like to upload your own dataset or explore our system's pre-uploaded datasets? Type \'exit\' to quit.")

    while continue_running:
        user_input = input("Message ChatDB: ")
        memory.append(user_input)

        # Exiting ChatDB
        if user_input.lower() == 'exit':
            continue_running = False
            print("Goodbye! Thank you for using ChatDB.")
            continue
        
        # Get keywords from user input
        keywords = match_query_pattern(user_input)
        print("Keywords:", keywords)

        if "UPLOAD" in keywords: # FROM JACOB: I THINK WE SHOULD MAKE THIS A MORE INTUITIVE PROCESS (If you type upload, ask what software and then ask for file path)
            try:
                if 'SQL' in keywords:
                    sql_upload(user_input, login_info)
                elif 'MONGODB' in keywords:
                    mongo_upload(user_input, login_info)
                else:
                    print('Please specify either SQL or NoSQL upload.')
            except FileNotFoundError as e:
                print("Couldn\'t find the file, please give an exact or relative file path")
        

        elif 'EXPLORE' in keywords:
            print('showing tables')
            sql_metadata = get_mysql_metadata(login_info)
            mongo_metadata = get_mongodb_metadata(login_info)

            explore_data(sql_metadata, mongo_metadata, connection, login_info)
            
        elif 'EXAMPLE' in keywords:
            # print('example in keywds')
            if 'SQL' in keywords:
                metadata = get_mysql_metadata(login_info)

                keywords_with_aggregates = find_keywords_for_examples(keywords, user_input)
                # print(keywords_with_aggregates)
                if 'JOIN' in keywords_with_aggregates:
                    display_join_queries(metadata, connection, keywords_with_aggregates)
                else:
                    display_queries(metadata, connection, keywords_with_aggregates)
            elif 'MONGODB' in keywords:
                metadata = get_mongodb_metadata(login_info)

                keywords_with_aggregates = find_keywords_for_examples_mongo(keywords, user_input)
                display_mongo_queries(metadata, login_info, keywords_with_aggregates)
            else:
                print("Please specify either SQL or MONGODB in your request for examples.")

        elif 'SELECT' in keywords or 'AGGREGATE' in keywords:
            if gen_queries.sql_or_nosql(user_input, login_info) == 'SQL':
                print('Generating an SQL query...')
                try:
                    gen_queries.execute_sql_query(user_input, keywords, login_info)
                except Exception as e:
                    print(f'Error generating query, try rephrasing your request. Error: \n{e}')
            elif gen_queries.sql_or_nosql(user_input, login_info) == 'MONGODB':
                print('Generating a MongoDB query...')
                try:
                    gen_queries.execute_mongo_query(user_input, keywords, login_info)
                except:
                    print(f'Error generating query, try rephrasing your request. Error: \n{e}')
            else:
                print('In your query, please specify which table/collection you would like to use.')

    return  


chatdb()

