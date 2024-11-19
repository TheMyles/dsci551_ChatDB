import pymysql
import pymongo
import sys

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
        query = input("Query: ")
        
        keywords = (query)

        if 'example' in keywords:
            response = (keywords)


        print(reponse)



    return  



chatdb()

