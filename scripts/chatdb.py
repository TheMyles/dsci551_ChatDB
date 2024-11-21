import pymysql
import pymongo
import sys
from input_process import match_query_pattern
from upload import sql_upload

"""
Setup MySQL DB
main py file
Functions in secondary py files
    NLP
    [Uploading
    Generating Example queries
    Generating queries] * 2 
"""

mongo_username = 'mdmolnar'
mongo_password = 'AtM0nG0d1452'

memory = []

def chatdb():
    continue_running = True

    while continue_running:
        reponse = ''
        user_input = input("Query: ")

        if user_input == 'exit':
            continue_running = False
            continue
        
        keywords = match_query_pattern(user_input)
        print("Keywords:", keywords)

        if "UPLOAD" in keywords:
            print('upload in kywds')
            if 'SQL' in keywords:
                print('SQL in keywords')
                sql_upload(user_input)

        if 'EXAMPLE' in keywords:
            print('example in keywds')
            response = (keywords)


        print(reponse)



    return  



chatdb()

