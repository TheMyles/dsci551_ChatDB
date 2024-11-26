import pymysql
import pymongo
import sys
from input_process import match_query_pattern
from upload import sql_upload, mongo_upload
import gen_queries

from generate_sql_examples_final import get_mysql_metadata
from generate_sql_examples_final import generate_sql_query
from generate_sql_examples_final import validate_query
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
<<<<<<< Updated upstream
    'password': "MySQLDBP455",
    'sql_database_name': "chatdb",
=======
    'password': "Bobo8128!",
    'database_name': "chatdb",
>>>>>>> Stashed changes
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
            metadata = get_mysql_metadata(login_info)
            # print(metadata)

            connection = pymysql.connect(
            host='localhost',
            user='root',
            password="Bobo8128!",
            database="chatdb"
            )

            keywords_without_example = [keyword for keyword in keywords if keyword != "EXAMPLE"]
            print(keywords_without_example)

            # List of words associated with 'AGGREGATE'
            aggregate_keywords = ["many", "sum", "average", "mean", "count", "total", "maximum", "minimum",
                      "min", "max", "avg", "median", "aggregate", "statistics", "metrics"]
            keywords_with_aggregates = keywords_without_example
            # Check if 'AGGREGATE' is in the keywords list
            if "AGGREGATE" in keywords_without_example:
                # Search for each word in the user_input and add to keywords_with_aggregate if found
                for word in aggregate_keywords:
                    if word.lower() in user_input.lower():  # Case insensitive search
                        keywords_with_aggregates.append(word)
            
            if "AGGREGATE" in keywords_with_aggregates:
                keywords_with_aggregates.remove("AGGREGATE")

            print(keywords_with_aggregates)
            
            # Generate and print 5 queries at a time
            for _ in range(5):
                while True:
                    sql_query, summary_text = generate_sql_query(metadata, connection)
                    
                    # Validate the query and ensure it uses the 'review' column
                    if sql_query.startswith("Error:") or not validate_query(sql_query, connection):
                        continue  # Retry if the query is invalid or fails
                    
                    # Check if all keywords are present in the query
                    if not all(keyword.lower() in sql_query.lower() for keyword in keywords_without_example):
                        continue  # Retry if the query does not contain all keywords
                    
                    # If valid and includes all keywords, print and break
                    print("\nGenerated Query:")
                    print(sql_query)
                    print("Summary:")
                    print(summary_text)

                    # # Create a cursor and execute the query
                    # cursor = connection.cursor()
                    # cursor.execute(sql_query)
                    
            #         # # Fetch and print the query result in tabular format
            #         # result = cursor.fetchall()  # Fetch all rows
            #         # column_names = [desc[0] for desc in cursor.description]  # Get column names
                    
            #         # print("Output:")
            #         # # Print the result in a tabular format using tabulate
            #         # print(tabulate(result, headers=column_names, tablefmt="pretty"))
                    break


            response = (keywords)

        elif 'SELECT' in keywords or 'AGGREGATE' in keywords:

            if gen_queries.sql_or_nosql(user_input, login_info) == 'SQL':
                gen_queries.execute_sql_query(user_input, keywords, login_info)


        print(reponse)



    return  



chatdb()

