import pymongo
import tabulate

def get_mongodb_metadata(login_info):
    metadata = {}

    # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']
    database_name = login_info['mongo_database_name']

    connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'

    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(connection_string)
        db = client[database_name]
        
        # Get all collection names
        collections = db.list_collection_names()
        
        for collection_name in collections:
            # print("=" * 20)  # Separator line
            # print(f"Collection: {collection_name}")
            
            # Sample documents from the collection to infer metadata
            collection = db[collection_name]
            sample_docs = list(collection.find({}, limit=100))  # Limit for performance
            
            # Infer metadata for each field in the collection
            field_metadata = {}
            for doc in sample_docs:
                for key, value in doc.items():
                    if key not in field_metadata:
                        field_metadata[key] = {
                            "type": type(value).__name__,  # Infer type from Python's type
                            "primary_key": key == "_id",  # MongoDB's primary key is typically "_id"
                            "unique_values": set()  # Store unique values as a set
                        }
                    # Add unique values if they are hashable
                    if isinstance(value, (int, float, str, bool, type(None))):  # Hashable types
                        field_metadata[key]["unique_values"].add(value)
            
            # Convert unique_values to a list (limit for performance)
            for field in field_metadata.values():
                field["unique_values"] = list(field["unique_values"])  # Limit to 5 unique values
            
            # Store metadata for the collection
            metadata[collection_name] = [
                {
                    "name": field,
                    "type": field_metadata[field]["type"],
                    "primary_key": field_metadata[field]["primary_key"],
                    "unique_values": field_metadata[field]["unique_values"]
                }
                for field in field_metadata
            ]
            
            # # Print metadata for debugging
            # for field in metadata[collection_name]:
            #     print(f"Field: {field['name']}, Type: {field['type']}, Primary Key: {field['primary_key']}, Unique Values: {field['unique_values']}")
        
        client.close()  # Close the connection after use
    except pymongo.errors.PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
    
    return metadata


# login_info = {
#     'endpoint': "localhost",
#     'username': "root",
#     'password': "Bobo8128!",
#     'sql_database_name': "chatdb",
#     'mongo_username': 'mdmolnar',
#     'mongo_password': 'AtM0nG0d1452',
#     'mongo_database_name': "ChatDB",
# }

import random
from pymongo import MongoClient

def generate_mongodb_query(metadata, client):
    templates_with_summaries = [
        # Generic find queries
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD>": "<NUMVALUE>"}},
            "summary": "Find all documents in <COLLECTION> where <FIELD> equals <NUMVALUE>."
        },
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD>": {"$ne": "<NUMVALUE>"}}},
            "summary": "Find all documents in <COLLECTION> where <FIELD> is not equal to <NUMVALUE>."
        },
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD>": "<STRVALUE>"}},
            "summary": "Find all documents in <COLLECTION> where <FIELD> equals <STRVALUE>."
        },
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD>": {"$regex": "<STRVALUE>", "$options": "i"}}},
            "summary": "Find all documents in <COLLECTION> where <FIELD> contains '<STRVALUE>'."
        },
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD1>": "<STRVALUE>", "<FIELD2>": "<NUMVALUE>"}},
            "summary": "Find all documents in <COLLECTION> where <FIELD1> equals <STRVALUE> and <FIELD2> equals <NUMVALUE>."
        },

        # Aggregation queries
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$match": {"<FIELD>": "<STRVALUE>"}},
                {"$group": {"_id": "$<GROUPFIELD>", "count": {"$sum": 1}}}
            ]},
            "summary": "Count the number of documents in <COLLECTION> grouped by <GROUPFIELD>, where <FIELD> equals <STRVALUE>."
        },
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$match": {"<FIELD>": {"$ne": "<NUMVALUE>"}}},
                {"$group": {"_id": "$<GROUPFIELD>", "count": {"$sum": 1}}}
            ]},
            "summary": "Count the number of documents in <COLLECTION> grouped by <GROUPFIELD>, where <FIELD> is not equal to <NUMVALUE>."
        },
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$match": {"<FIELD>": {"$gt": "<NUMVALUE>"}}},
                {"$group": {"_id": "$<GROUPFIELD>", "average": {"$avg": "$<NUMFIELD>"}}}
            ]},
            "summary": "Find the average value of <NUMFIELD> grouped by <GROUPFIELD> in <COLLECTION>, where <FIELD> is greater than <NUMVALUE>."
        },

        # Sorting and limiting
        {
            "query": {"find": "<COLLECTION>", "filter": {"<FIELD>": "<STRVALUE>"}, "sort": [("<FIELD>", 1)], "limit": "<NUMVALUE>"},
            "summary": "Find documents in <COLLECTION> where <FIELD> equals <STRVALUE>, sorted in ascending order, limited to <NUMVALUE> results."
        },
        {
            "query": {"find": "<COLLECTION>", "filter": {}, "sort": [("<FIELD>", -1)], "limit": "<NUMVALUE>"},
            "summary": "Find documents in <COLLECTION> sorted by <FIELD> in descending order, limited to <NUMVALUE> results."
        },

        # Advanced group queries
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$group": {"_id": "$<GROUPFIELD>", "sum": {"$sum": "$<NUMFIELD>"}}}
            ]},
            "summary": "Find the sum of <NUMFIELD> grouped by <GROUPFIELD> in <COLLECTION>."
        },
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$group": {"_id": "$<GROUPFIELD>", "max": {"$max": "$<NUMFIELD>"}}}
            ]},
            "summary": "Find the maximum value of <NUMFIELD> grouped by <GROUPFIELD> in <COLLECTION>."
        },
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$group": {"_id": "$<GROUPFIELD>", "min": {"$min": "$<NUMFIELD>"}}}
            ]},
            "summary": "Find the minimum value of <NUMFIELD> grouped by <GROUPFIELD> in <COLLECTION>."
        },
        {
            "query": {"aggregate": "<COLLECTION>", "pipeline": [
                {"$match": {"<FIELD>": {"$gte": "<NUMVALUE1>", "$lte": "<NUMVALUE2>"}}},
                {"$group": {"_id": "$<GROUPFIELD>", "count": {"$sum": 1}}}
            ]},
            "summary": "Count the number of documents in <COLLECTION> grouped by <GROUPFIELD>, where <FIELD> is between <NUMVALUE1> and <NUMVALUE2>."
        }
    ]

    # Pick a random collection
    collection_name = 'UW_std_person'
    fields = metadata[collection_name]  # Get field metadata for the collection
    
    # # Check for numeric fields
    # numeric_fields = [field for field in fields if field["type"] in ("int", "float", "decimal")]
    # has_numeric = bool(numeric_fields)

    # Check for numeric fields excluding 'id' fields
    numeric_fields = [
        field for field in fields
        if field["type"] in ("int", "float", "decimal") and 'id' not in field["name"].lower()
    ]
    has_numeric = bool(numeric_fields)
    
    # Pick a random template
    templates = templates_with_summaries
    template_data = random.choice(templates)
    query_template = str(template_data["query"])
    summary_template = template_data["summary"]
    
    # Replace <COLLECTION>
    query_template = query_template.replace("<COLLECTION>", collection_name)
    summary_template = summary_template.replace("<COLLECTION>", collection_name)
    
    # Replace <NUMFIELD> and <NUMVALUE>
    while "<NUMFIELD>" in query_template:
        if not numeric_fields:
            return "Error: No valid numeric fields available in the selected collection.", None
        num_field = random.choice(numeric_fields)
        query_template = query_template.replace("<NUMFIELD>", num_field["name"], 1)
        summary_template = summary_template.replace("<NUMFIELD>", num_field["name"], 1)
    
    while "<NUMVALUE>" in query_template:
        if numeric_fields:
            num_field = random.choice(numeric_fields)
            num_value = random.choice(num_field["unique_values"]) if num_field["unique_values"] else random.randint(1, 100)
        else:
            num_value = random.randint(1, 100)
        query_template = query_template.replace("<NUMVALUE>", str(num_value), 1)
        summary_template = summary_template.replace("<NUMVALUE>", str(num_value), 1)
    
    # Replace <FIELD> and <STRVALUE>
    while "<FIELD>" in query_template:
        field = random.choice(fields)
        query_template = query_template.replace("<FIELD>", field["name"], 1)
        summary_template = summary_template.replace("<FIELD>", field["name"], 1)
    
    while "<STRVALUE>" in query_template:
        str_fields = [field for field in fields if field["type"] == "string"]
        if not str_fields:
            return "Error: No valid string fields available in the selected collection.", None
        str_field = random.choice(str_fields)
        str_value = random.choice(str_field["unique_values"]) if str_field["unique_values"] else "default"
        query_template = query_template.replace("<STRVALUE>", str_value, 1)
        summary_template = summary_template.replace("<STRVALUE>", str_value, 1)
    
    # Replace <FIELD1> and <FIELD2>
    while "<FIELD1>" in query_template:
        field1 = random.choice(fields)
        query_template = query_template.replace("<FIELD1>", field1["name"], 1)
        summary_template = summary_template.replace("<FIELD1>", field1["name"], 1)
    
    while "<FIELD2>" in query_template:
        field2 = random.choice([field for field in fields if field != field1])
        query_template = query_template.replace("<FIELD2>", field2["name"], 1)
        summary_template = summary_template.replace("<FIELD2>", field2["name"], 1)
    
    # Replace <GROUPFIELD>
    while "<GROUPFIELD>" in query_template:
        group_field = random.choice(fields)["name"]
        query_template = query_template.replace("<GROUPFIELD>", group_field, 1)
        summary_template = summary_template.replace("<GROUPFIELD>", group_field, 1)
    
    # Replace <NUMVALUE1> and <NUMVALUE2> for ranges
    while "<NUMVALUE1>" in query_template or "<NUMVALUE2>" in query_template:
        if numeric_fields:
            num_field = random.choice(numeric_fields)
            num_value1 = random.choice(num_field["unique_values"]) if num_field["unique_values"] else random.randint(1, 50)
            num_value2 = random.choice(num_field["unique_values"]) if num_field["unique_values"] else random.randint(51, 100)
        else:
            num_value1, num_value2 = random.randint(1, 50), random.randint(51, 100)
        query_template = query_template.replace("<NUMVALUE1>", str(num_value1), 1).replace("<NUMVALUE2>", str(num_value2), 1)
        summary_template = summary_template.replace("<NUMVALUE1>", str(num_value1), 1).replace("<NUMVALUE2>", str(num_value2), 1)
    
    return query_template, summary_template


def find_keywords_for_examples_mongo(keywords, user_input):
    keywords_without_example = [keyword for keyword in keywords if keyword != "EXAMPLE"]
    keywords_without_example.remove("MONGODB")
    if "SELECT" in keywords_without_example:
        keywords_without_example.remove("SELECT")
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
    
    return keywords_with_aggregates


# import pymongo
# from pymongo.errors import PyMongoError
# from tabulate import tabulate

# def validate_mongo_query(query, db):
#     try:
#         # Check if the query is a string and evaluate it into a dictionary
#         if isinstance(query, str):
#             query = eval(query)

#         # Handle "find" queries
#         if "find" in query:
#             collection_name = query["find"]
#             filter_condition = query.get("filter", {})
#             projection = query.get("projection", None)
#             limit = query.get("limit", 15)  # Default limit to 15 if not provided

#             # Ensure limit is an integer
#             if not isinstance(limit, int):
#                 limit = int(limit)  # Attempt to convert to integer, or raise an error

#             # Execute the query
#             cursor = db[collection_name].find(filter_condition, projection).limit(limit)
#             results = list(cursor)  # Fetch results as a list
#             return bool(results)  # Return True if results are non-empty, False otherwise

#         # Handle "aggregate" queries
#         elif "aggregate" in query:
#             collection_name = query["aggregate"]
#             pipeline = query.get("pipeline", [])

#             # Add a $limit stage to the pipeline if it doesn't already exist
#             if not any("$limit" in stage for stage in pipeline):
#                 pipeline.append({"$limit": 15})

#             # Execute the aggregation pipeline
#             cursor = db[collection_name].aggregate(pipeline)
#             results = list(cursor)  # Fetch results as a list
#             return bool(results)  # Return True if results are non-empty, False otherwise

#         # Unsupported query type
#         else:
#             print("Unsupported query type.")
#             return False

#     except Exception as e:
#         print(f"Error during query validation: {e}")
#         return False


# # Function to display and execute queries in MongoDB
# def display_mongo_queries(metadata, login_info, keywords_without_example):
#     # MongoDB credentials and connection string
#     mongo_username = login_info['mongo_username']
#     mongo_password = login_info['mongo_password']
#     database_name = login_info['mongo_database_name']

#     connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'

#     # Connect to MongoDB
#     client = pymongo.MongoClient(connection_string)
#     db = client[database_name]
    
#     # List to store the generated queries
#     queries_list = []

#     # Generate and print 5 queries at a time
#     for _ in range(5):
#         while True:
#             mongo_query, summary_text = generate_mongodb_query(metadata, client)

#             # Validate the query
#             if mongo_query.startswith("Error:") or not validate_mongo_query(mongo_query, db):
#                 continue  # Retry if the query is invalid or fails

#             # Check if all keywords are present in the query
#             if not all(keyword.lower() in str(mongo_query).lower() for keyword in keywords_without_example):
#                 continue  # Retry if the query does not contain all keywords

#             # Store the valid query and its summary in the list
#             queries_list.append((mongo_query, summary_text))

#             # Print the generated query and summary
#             print("\nGenerated Query:")
#             print(mongo_query)
#             print("Summary:")
#             print(summary_text)

#             break  # Exit the while loop once a valid query is found

#     # Print the queries list and prompt the user to select a query
#     print("\nSelect a query to run (1-5):")
#     for i, (query, summary) in enumerate(queries_list, 1):
#         print(f"{i}. {summary}")  # Print the summary for each query

#     # Get the user's choice
#     user_choice = int(input("Enter the number of the query you want to run: ")) - 1  # Adjust for 0-based index

#     # Ensure the choice is valid
#     if 0 <= user_choice < len(queries_list):
#         selected_query, selected_summary = queries_list[user_choice]
#         # Execute the selected query
#         execute_mongo_query(selected_query, client, database_name)
#     else:
#         print("Invalid choice. Please select a number between 1 and 5.")


# # Function to execute MongoDB queries
# def execute_mongo_query(query, client, database_name):
#     try:
#         if "find" in query:
#             collection_name = query["find"]
#             filter_query = query.get("filter", {})
#             limit = query.get("limit", 0)
#             sort = query.get("sort", [])

#             # Execute the query
#             collection = client[database_name][collection_name]
#             results = list(collection.find(filter_query).sort(sort).limit(limit))
#             if results:
#                 # Print the results in tabular format using tabulate
#                 print("Output:")
#                 print(tabulate(results, headers="keys", tablefmt="pretty"))
#             else:
#                 print("No results found.")

#         elif "aggregate" in query:
#             collection_name = query["aggregate"]
#             pipeline = query.get("pipeline", [])

#             # Execute the aggregation pipeline
#             collection = client[database_name][collection_name]
#             results = list(collection.aggregate(pipeline))
#             if results:
#                 # Print the results in tabular format using tabulate
#                 print("Output:")
#                 print(tabulate(results, headers="keys", tablefmt="pretty"))
#             else:
#                 print("No results found.")

#         else:
#             print("Unsupported query type.")

#     except PyMongoError as e:
#         print(f"Error executing MongoDB query: {e}")



# import pymongo
# from tabulate import tabulate
# import random


# def display_mongo_queries(metadata, login_info, keywords_without_example):
#     # MongoDB credentials and connection string
#     mongo_username = login_info['mongo_username']
#     mongo_password = login_info['mongo_password']
#     database_name = login_info['mongo_database_name']
#     connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.mongodb.net/'

#     # Connect to MongoDB
#     client = pymongo.MongoClient(connection_string)
#     db = client[database_name]

#     # List to store the generated queries
#     queries_list = []

#     # Generate and print 5 queries at a time
#     for _ in range(5):
#         while True:
#             mongo_query, summary_text = generate_mongodb_query(metadata, db)

#             # Check if all keywords are present in the query
#             if mongo_query.startswith("Error:"):
#                 continue  # Retry if the query is invalid or fails
#             if not all(keyword.lower() in str(mongo_query).lower() for keyword in keywords_without_example):
#                 continue  # Retry if the query does not contain all keywords

#             # Store the valid query and its summary in the list
#             queries_list.append((mongo_query, summary_text))

#             # Print the generated query and summary
#             print("\nGenerated Query:")
#             print(mongo_query)
#             print("Summary:")
#             print(summary_text)

#             break  # Exit the while loop once a valid query is found

#     # Print the queries list and prompt the user to select a query
#     print("\nSelect a query to run (1-5):")
#     for i, (_, summary) in enumerate(queries_list, 1):
#         print(f"{i}. {summary}")  # Print the summary for each query

#     # Get the user's choice
#     user_choice = int(input("Enter the number of the query you want to run: ")) - 1  # Adjust for 0-based index

#     # Ensure the choice is valid
#     if 0 <= user_choice < len(queries_list):
#         selected_query, selected_summary = queries_list[user_choice]
#         # Execute the selected query
#         execute_mongodb_query(selected_query, login_info)
#     else:
#         print("Invalid choice. Please select a number between 1 and 5.")

#     client.close()  # Close the connection


# def execute_mongodb_query(query, login_info):
#     # MongoDB credentials and connection string
#     mongo_username = login_info['mongo_username']
#     mongo_password = login_info['mongo_password']
#     database_name = login_info['mongo_database_name']
#     connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.mongodb.net/'

#     # Connect to MongoDB
#     client = pymongo.MongoClient(connection_string)
#     db = client[database_name]
#     collection = db[query.get('find') if 'find' in query else query.get('aggregate')]

#     if 'find' in query:
#         filter_ = query.get('filter', {})
#         sort = query.get('sort', None)
#         limit = query.get('limit', None)

#         cursor = collection.find(filter_)
#         if sort:
#             cursor = cursor.sort(sort)
#         if limit:
#             cursor = cursor.limit(limit)

#         # Fetch and display results
#         results = list(cursor)
#     elif 'aggregate' in query:
#         pipeline = query['pipeline']
#         results = list(collection.aggregate(pipeline))
#     else:
#         results = []

#     # Display results
#     if results:
#         print("Output:")
#         print(tabulate(results, headers="keys", tablefmt="pretty"))
#     else:
#         print("No results found.")

#     client.close()  # Close the connection

# import pymongo
# import random
# from bson.json_util import dumps


# def generate_and_execute_mongo_queries_with_keywords(metadata, login_info, keywords_without_example):
#     """
#     Generate 5 MongoDB queries, check for required keywords, display their summaries,
#     and allow the user to choose one to execute.

#     Parameters:
#     metadata: dict - Metadata of MongoDB collections and fields.
#     login_info: dict - Connection details for MongoDB.
#     keywords_without_example: list - List of keywords that must appear in the query.
#     """
#     # MongoDB credentials and connection string
#     mongo_username = login_info['mongo_username']
#     mongo_password = login_info['mongo_password']
#     database_name = login_info['mongo_database_name']
#     connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'

#     # Connect to MongoDB
#     client = pymongo.MongoClient(connection_string)
#     db = client[database_name]

#     def execute_mongodb_query(query, db):
#         try:
#             if "find" in query:
#                 collection_name = query["find"]
#                 filter_condition = query.get("filter", {})
#                 projection = query.get("projection", None)
#                 cursor = db[collection_name].find(filter_condition, projection).limit(15)  # Limit results to 15
#                 return list(cursor)  # Return the query result as a list
#             elif "aggregate" in query:
#                 collection_name = query["aggregate"]
#                 pipeline = query.get("pipeline", [])
#                 # Add a $limit stage to the aggregation pipeline if it doesn't already exist
#                 if not any(stage.get("$limit") for stage in pipeline):
#                     pipeline.append({"$limit": 15})
#                 cursor = db[collection_name].aggregate(pipeline)
#                 return list(cursor)  # Return the query result as a list
#             else:
#                 raise ValueError("Unsupported query type.")
#         except Exception as e:
#             return f"Error: {str(e)}"

#     results = []

#     while len(results) < 5:  # Ensure we collect 5 queries with non-empty results
#         query, summary = generate_mongodb_query(metadata, db)
#         # print("\nGenerated Query:")
#         # print(query)
#         # Check if all keywords are present in the query
#         if not all(keyword.lower() in str(query).lower() for keyword in keywords_without_example):

#             continue  # Retry if the query does not contain all keywords
#         else:
#             print(query)
#         if query.startswith("Error:"):
#             continue  # Generate a new query if there's an error
#         result = execute_mongodb_query(eval(query), db)
#         if isinstance(result, str) and result.startswith("Error:"):
#             continue  # Generate a new query if execution fails
#         if not result:
#             continue  # Skip queries that return an empty result set
#         results.append({"query": query, "summary": summary, "output": result})

#     # Display the generated queries
#     print("\nGenerated Queries:")
#     for idx, res in enumerate(results):
#         print(f"{idx + 1}. {res['summary']}")

#     # Prompt the user to choose a query
#     user_choice = int(input("\nEnter the number of the query you want to run (1-5): ")) - 1

#     # Validate the choice and execute the query
#     if 0 <= user_choice < len(results):
#         chosen_query = results[user_choice]
#         print("\nExecuting the chosen query:")
#         print(dumps(chosen_query["query"], indent=2))
#         print("\nQuery Results:")
#         print(dumps(chosen_query["output"], indent=2))
#     else:
#         print("Invalid choice. Please select a number between 1 and 5.")

#     client.close()  # Close the MongoDB connection


import pymongo
from bson.json_util import dumps

def generate_and_display_queries(login_info, metadata, keywords_without_example):
    """
    Generate 5 MongoDB queries, display their summaries, and allow the user to choose one to execute.

    Parameters:
    login_info: dict - MongoDB connection details.
    metadata: dict - Metadata of MongoDB collections and fields.
    """
    # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']
    database_name = login_info['mongo_database_name']
    connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'

    # Connect to MongoDB
    client = pymongo.MongoClient(connection_string)
    db = client[database_name]

    # Function to execute MongoDB queries
    def execute_mongodb_query(query, db):
        try:
            if "find" in query:
                collection_name = query["find"]
                filter_condition = query.get("filter", {})
                projection = query.get("projection", None)
                cursor = db[collection_name].find(filter_condition, projection).limit(15)
                return list(cursor)
            elif "aggregate" in query:
                collection_name = query["aggregate"]
                pipeline = query.get("pipeline", [])
                if not any(stage.get("$limit") for stage in pipeline):
                    pipeline.append({"$limit": 15})
                cursor = db[collection_name].aggregate(pipeline)
                return list(cursor)
            else:
                raise ValueError("Unsupported query type.")
        except Exception as e:
            return f"Error: {str(e)}"

    # Generate, execute, and collect 5 MongoDB queries with results
    results = []
    exclusion_words = ['$ne']
    while len(results) < 5:  # Ensure 5 queries with non-empty results
        query, summary = generate_mongodb_query(metadata, client)
        if any(exclusion_word.lower() in query.lower() for exclusion_word in exclusion_words):
            continue
        # Check if all keywords are present in the query
        if not all(keyword.lower() in str(query).lower() for keyword in keywords_without_example):
            continue  # Retry if the query does not contain all keywords
        if query.startswith("Error:"):
            continue
        result = execute_mongodb_query(eval(query), db)
        if isinstance(result, str) and result.startswith("Error:"):
            continue
        if not result:
            continue
        results.append({"query": query, "summary": summary, "output": result})

    # Display query summaries for user selection
    print("\nGenerated Queries:")
    for idx, res in enumerate(results):
        print(f"{idx + 1}. {res['summary']}")

    # Prompt user to choose a query
    user_choice = int(input("\nEnter the number of the query you want to view the output for (1-5): ")) - 1

    # Validate choice and display output
    if 0 <= user_choice < len(results):
        chosen_result = results[user_choice]
        print("\nSelected Query:")
        print(chosen_result["query"])
        print("\nSummary:")
        print(chosen_result["summary"])
        print("\nOutput:")
        print(dumps(chosen_result["output"], indent=4))
    else:
        print("Invalid choice. Please select a number between 1 and 5.")

    client.close()  # Close the MongoDB connection
