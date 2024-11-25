import pymysql
import pymongo
import sys
from input_process import match_query_pattern
from upload import sql_upload, mongo_upload
import gen_queries

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
            print('example in keywds')
            response = (keywords)

        elif 'SELECT' in keywords or 'AGGREGATE' in keywords:

            if gen_queries.sql_or_nosql(user_input, login_info) == 'SQL':
                gen_queries.execute_sql_query(user_input, keywords, login_info)


        print(reponse)



    return  



chatdb()

