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


# login_info = {
#     'endpoint': "localhost",
#     'username': "root",
#     'password': "MySQLDBP455",
#     'database_name': "chatdb",
#     'mongo_username': 'mdmolnar',
#     'mongo_password': 'AtM0nG0d1452'
# }

login_info = {
    'endpoint': "localhost",
    'username': "root",
    'password': "Bobo8128!",
    'sql_database_name': "chatdb",
    'mongo_username': 'mdmolnar',
    'mongo_password': 'AtM0nG0d1452',
    'mongo_database_name': "ChatDB",
}

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
        reponse = ''
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

        elif 'SHOW' in keywords:
            print('showing tables')
            
        elif 'EXAMPLE' in keywords:
            # print('example in keywds')
            metadata = get_mysql_metadata(login_info)

            keywords_with_aggregates = find_keywords_for_examples(keywords, user_input)
            # print(keywords_with_aggregates)

            display_queries(metadata, connection, keywords_with_aggregates)

        elif 'SELECT' in keywords or 'AGGREGATE' in keywords:

            if gen_queries.sql_or_nosql(user_input, login_info) == 'SQL':
                gen_queries.execute_sql_query(user_input, keywords, login_info)


        print(reponse)



    return  



chatdb()

