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

from mongo_examples_testing import get_mongodb_metadata

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

        if "UPLOAD" in keywords:
            print('upload in kywds')
            if 'SQL' in keywords:
                print('SQL in keywords')
                sql_upload(user_input, login_info)
            elif 'MONGODB' in keywords:
                print('Mongo in kywds')
                mongo_upload(user_input, login_info)
            else:
                print('Please specify either SQL or NoSQL upload.')

        elif 'EXPLORE' in keywords:
            print('showing tables')
            sql_metadata = get_mysql_metadata(login_info)
            mongo_metadata = get_mongodb_metadata(login_info)

            explore_data(sql_metadata, mongo_metadata, connection)
            
        elif 'EXAMPLE' in keywords:
            # print('example in keywds')
            if 'SQL' in keywords:
                metadata = get_mysql_metadata(login_info)

                keywords_with_aggregates = find_keywords_for_examples(keywords, user_input)
                # print(keywords_with_aggregates)

                display_queries(metadata, connection, keywords_with_aggregates)
            elif 'MONGODB' in keywords:
                pass
            else:
                print("Please specify either SQL or MONGODB in your request.")

        elif 'SELECT' in keywords or 'AGGREGATE' in keywords:
            if gen_queries.sql_or_nosql(user_input, login_info) == 'SQL':
                print('Generating an SQL query...')
                gen_queries.execute_sql_query(user_input, keywords, login_info)
            elif gen_queries.sql_or_nosql(user_input, login_info) == 'MONGODB':
                print('Generating a MongoDB query...')
            else:
                print('In your query, please specify which table/collection you would like to use.')



    return  



chatdb()

