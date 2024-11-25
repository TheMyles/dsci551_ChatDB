import pymongo

def get_mongodb_metadata(login_info):
    metadata = {}

    # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']
    database_name = login_info['database_name']

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


# Example usage
login_info = {
    'endpoint': "localhost",
    'username': "root",
    'password': "Bobo8128!",
    'database_name': "ChatDB",
    'mongo_username': 'mdmolnar',
    'mongo_password': 'AtM0nG0d1452'
}

metadata = get_mongodb_metadata(login_info)
print(metadata)


    # templates_with_summaries = [
    #     # Simple queries with comparison operators
    #     {
    #         "query": { "<NUMCOLUMN>": { "$eq": "<NUMVALUE>" } },
    #         "summary": "Find documents where <NUMCOLUMN> equals <NUMVALUE>."
    #     },
    #     {
    #         "query": { "<NUMCOLUMN>": { "$gt": "<NUMVALUE>" } },
    #         "summary": "Find documents where <NUMCOLUMN> is greater than <NUMVALUE>."
    #     },
    #     {
    #         "query": { "<COLUMN>": { "$regex": "<STRVALUE>" } },
    #         "summary": "Find documents where <COLUMN> contains '<STRVALUE>'."
    #     },
    #     {
    #         "query": { "<COLUMN>": { "$in": ["<STRVALUE>", "<STRVALUE>", "<STRVALUE>"] } },
    #         "summary": "Find documents where <COLUMN> matches one of the given values."
    #     },
    #     # Aggregation queries
    #     {
    #         "query": [ { "$group": { "_id": "$<COLUMN>", "count": { "$sum": 1 } } } ],
    #         "summary": "Count the number of rows grouped by <COLUMN>."
    #     },
    #     {
    #         "query": [ { "$group": { "_id": "$<COLUMN>", "total": { "$sum": "$<NUMCOLUMN>" } } } ],
    #         "summary": "Find the sum of <NUMCOLUMN> grouped by <COLUMN>."
    #     },
    #     {
    #         "query": [ { "$group": { "_id": "$<COLUMN>", "average": { "$avg": "$<NUMCOLUMN>" } } } ],
    #         "summary": "Find the average value of <NUMCOLUMN> grouped by <COLUMN>."
    #     },
    #     {
    #         "query": [ { "$group": { "_id": "$<COLUMN>", "max": { "$max": "$<NUMCOLUMN>" } } } ],
    #         "summary": "Find the maximum value of <NUMCOLUMN> grouped by <COLUMN>."
    #     },
    #     {
    #         "query": [ { "$group": { "_id": "$<COLUMN>", "min": { "$min": "$<NUMCOLUMN>" } } } ],
    #         "summary": "Find the minimum value of <NUMCOLUMN> grouped by <COLUMN>."
    #     },
    #     {
    #         "query": [
    #             { "$group": { "_id": "$<COLUMN>", "count": { "$sum": 1 } } },
    #             { "$match": { "count": { "$gt": "<NUMVALUE>" } } }
    #         ],
    #         "summary": "Find groups of <COLUMN> where the count of rows is greater than <NUMVALUE>."
    #     },
    #     {
    #         "query": [
    #             { "$group": { "_id": "$<COLUMN>", "average": { "$avg": "$<NUMCOLUMN>" } } },
    #             { "$match": { "average": { "$gt": "<NUMVALUE>" } } }
    #         ],
    #         "summary": "Find groups of <COLUMN> where the average value of <NUMCOLUMN> is greater than <NUMVALUE>."
    #     },
    #     {
    #         "query": [
    #             { "$match": { "<COLUMN>": { "$regex": "<STRVALUE>" } } },
    #             { "$group": { "_id": "$<COLUMN>", "total": { "$sum": "$<NUMCOLUMN>" } } }
    #         ],
    #         "summary": "Find the sum of <NUMCOLUMN> grouped by <COLUMN>, where <COLUMN> contains '<STRVALUE>'."
    #     },
    #     {
    #         "query": [
    #             { "$match": { "<COLUMN>": { "$in": ["<STRVALUE>", "<STRVALUE>", "<STRVALUE>"] } } },
    #             { "$group": { "_id": "$<COLUMN>", "max": { "$max": "$<NUMCOLUMN>" } } }
    #         ],
    #         "summary": "Find the maximum value of <NUMCOLUMN> grouped by <COLUMN>, where <COLUMN> matches one of the given values."
    #     },
    #     {
    #         "query": [
    #             { "$match": { "<COLUMN>": { "$eq": "<STRVALUE>" } } },
    #             { "$group": { "_id": "$<COLUMN>", "count": { "$sum": 1 } } },
    #             { "$sort": { "count": -1 } }
    #         ],
    #         "summary": "Count rows grouped by <COLUMN>, filtered by <STRVALUE>, and sorted by the count in descending order."
    #     },
    #     {
    #         "query": [
    #             { "$match": { "<NUMCOLUMN>": { "$gte": "<NUMVALUE>", "$lte": "<NUMVALUE>" } } },
    #             { "$group": { "_id": "$<COLUMN>", "count": { "$sum": 1 } } }
    #         ],
    #         "summary": "Count rows grouped by <COLUMN>, where <NUMCOLUMN> falls between <NUMVALUE> and <NUMVALUE>."
    #     },
    #     {
    #         "query": [
    #             { "$group": { "_id": "$<COLUMN>", "total": { "$sum": "$<NUMCOLUMN>" } } },
    #             { "$match": { "total": { "$gt": "<NUMVALUE>" } } }
    #         ],
    #         "summary": "Find groups of <COLUMN> where the sum of <NUMCOLUMN> is greater than <NUMVALUE>."
    #     }
    # ]


import random

# import random

# def generate_mongo_query(metadata):
#     templates_with_summaries = [
#         # Simple equality
#         {
#             "query": { "<COLUMN>": "<STRVALUE>" },
#             "summary": "Find documents where <COLUMN> equals <STRVALUE>."
#         },
#         # $in operator
#         {
#             "query": { "<COLUMN>": { "$in": ["<STRVALUE>", "<STRVALUE>", "<STRVALUE>"] } },
#             "summary": "Find documents where <COLUMN> matches one of the given values."
#         },
#         # $ne operator
#         {
#             "query": { "<COLUMN>": { "$ne": "<STRVALUE>" } },
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#         # Logical AND
#         {
#             "query": { "<COLUMN1>": "<STRVALUE1>", "<COLUMN2>": "<STRVALUE2>" },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> equals <STRVALUE2>."
#         },
#         # Logical OR
#         {
#             "query": { "$or": [{ "<COLUMN1>": "<STRVALUE1>" }, { "<COLUMN2>": "<STRVALUE2>" }] },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
#         },
#         # Combination of $in and equality
#         {
#             "query": { "<COLUMN1>": { "$in": ["<STRVALUE1>", "<STRVALUE2>"] }, "<COLUMN2>": "<STRVALUE3>" },
#             "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # $in for range filtering (e.g., years in a range)
#         {
#             "query": { "<COLUMN>": { "$in": ["Year_1", "Year_2", "Year_3", "Year_4"] } },
#             "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_1 to Year_4)."
#         },
#         # $in with multiple conditions
#         {
#             "query": { "<COLUMN>": { "$in": ["<STRVALUE1>", "<STRVALUE2>"] }, "<COLUMN2>": "<STRVALUE3>" },
#             "summary": "Find documents where <COLUMN> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # $and with $in
#         {
#             "query": { "$and": [{ "<COLUMN1>": { "$in": ["<STRVALUE1>", "<STRVALUE2>"] } }, { "<COLUMN2>": "<STRVALUE3>" }] },
#             "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # Logical NOT
#         {
#             "query": { "<COLUMN>": { "$not": { "$eq": "<STRVALUE>" } } },
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#         # Combination of $or and equality
#         {
#             "query": { "$or": [{ "<COLUMN1>": "<STRVALUE1>" }, { "<COLUMN2>": "<STRVALUE2>" }] },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
#         },
#         # Filtering on multiple conditions
#         {
#             "query": { "<COLUMN1>": "<STRVALUE1>", "<COLUMN2>": { "$in": ["<STRVALUE2>", "<STRVALUE3>"] } },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
#         },
#         # Range-based filtering with $in
#         {
#             "query": { "<COLUMN>": { "$in": ["Year_6", "Year_7", "Year_8", "Year_9", "Year_12"] } },
#             "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_6 to Year_12)."
#         },
#         # Multiple filters with $and and $or
#         {
#             "query": { "$and": [{ "$or": [{ "<COLUMN1>": "<STRVALUE1>" }, { "<COLUMN2>": "<STRVALUE2>" }] }, { "<COLUMN3>": { "$ne": "<STRVALUE3>" } }] },
#             "summary": "Find documents where either <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>, and <COLUMN3> does not equal <STRVALUE3>."
#         },
#         # Nested conditions
#         {
#             "query": { "$and": [{ "<COLUMN1>": "<STRVALUE1>" }, { "<COLUMN2>": { "$in": ["<STRVALUE2>", "<STRVALUE3>"] } }] },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
#         },
#     ]

#     # Pick a random collection
#     collection_name = random.choice(list(metadata.keys()))
#     fields = metadata[collection_name]  # Get metadata for fields in the collection

#     # Filter numeric and string fields
#     numeric_fields = [field for field in fields if field["type"] in ("int", "float")]
#     string_fields = [field for field in fields if field["type"] == "str"]

#     # Pick a random template
#     template_data = random.choice(templates_with_summaries)
#     query = template_data["query"]
#     summary = template_data["summary"]

#     # Replace placeholders
#     if "<COLUMN>" in str(query):
#         column = random.choice(fields)
#         query = str(query).replace("<COLUMN>", column["name"])
#         summary = summary.replace("<COLUMN>", column["name"])
    
#     if "<COLUMN1>" in str(query):
#         column1 = random.choice(fields)
#         query = str(query).replace("<COLUMN1>", column1["name"])
#         summary = summary.replace("<COLUMN1>", column1["name"])
    
#     if "<COLUMN2>" in str(query):
#         column2 = random.choice(fields)
#         query = str(query).replace("<COLUMN2>", column2["name"])
#         summary = summary.replace("<COLUMN2>", column2["name"])
    
#     if "<STRVALUE>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value = random.choice(str_column["unique_values"])
#             else:
#                 str_value = "default"  # Default string value
#             query = str(query).replace("<STRVALUE>", str_value, 1)  # Replace one instance at a time
#             summary = summary.replace("<STRVALUE>", str(str_value), 1)
    
#     if "<STRVALUE1>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value1 = random.choice(str_column["unique_values"])
#             else:
#                 str_value1 = "default"  # Default string value
#             query = str(query).replace("<STRVALUE1>", str_value1, 1)
#             summary = summary.replace("<STRVALUE1>", str(str_value1), 1)
    
#     if "<STRVALUE2>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value2 = random.choice(str_column["unique_values"])
#             else:
#                 str_value2 = "default"  # Default string value
#             query = str(query).replace("<STRVALUE2>", str_value2, 1)
#             summary = summary.replace("<STRVALUE2>", str(str_value2), 1)
    
#     if "<STRVALUE3>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value3 = random.choice(str_column["unique_values"])
#             else:
#                 str_value3 = "default"  # Default string value
#             query = str(query).replace("<STRVALUE3>", str_value3, 1)
#             summary = summary.replace("<STRVALUE3>", str(str_value3), 1)

#     return eval(query), summary

# import random

# def generate_mongo_query(metadata):
#     templates_with_summaries = [
#         # Simple equality
#         {
#             "query": { "<COLUMN>": "<STRVALUE>" },
#             "summary": "Find documents where <COLUMN> equals <STRVALUE>."
#         },
#         # $in operator
#         {
#             "query": { "<COLUMN>": { "$in": ["<STRVALUE>", "<STRVALUE>", "<STRVALUE>"] } },
#             "summary": "Find documents where <COLUMN> matches one of the given values."
#         },
#         # $ne operator
#         {
#             "query": { "<COLUMN>": { "$ne": "<STRVALUE>" } },
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#         # Logical AND
#         {
#             "query": { "<COLUMN1>": "<STRVALUE1>", "<COLUMN2>": "<STRVALUE2>" },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> equals <STRVALUE2>."
#         },
#         # Logical OR
#         {
#             "query": { "$or": [{ "<COLUMN1>": "<STRVALUE1>" }, { "<COLUMN2>": "<STRVALUE2>" }] },
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
#         },
#         # Logical NOT
#         {
#             "query": { "<COLUMN>": { "$not": { "$eq": "<STRVALUE>" } } },
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#     ]

#     # Pick a random collection
#     collection_name = random.choice(list(metadata.keys()))
#     fields = metadata[collection_name]  # Get metadata for fields in the collection

#     # Filter string fields
#     string_fields = [field for field in fields if field["type"] == "str"]

#     # Pick a random template
#     template_data = random.choice(templates_with_summaries)
#     query = template_data["query"]
#     summary = template_data["summary"]

#     # Replace placeholders
#     while "<COLUMN>" in str(query):
#         column = random.choice(fields)
#         query = eval(str(query).replace("<COLUMN>", column["name"]))
#         summary = summary.replace("<COLUMN>", column["name"])

#     while "<COLUMN1>" in str(query):
#         column1 = random.choice(fields)
#         query = eval(str(query).replace("<COLUMN1>", column1["name"]))
#         summary = summary.replace("<COLUMN1>", column1["name"])

#     while "<COLUMN2>" in str(query):
#         column2 = random.choice(fields)
#         query = eval(str(query).replace("<COLUMN2>", column2["name"]))
#         summary = summary.replace("<COLUMN2>", column2["name"])

#     while "<STRVALUE>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value = random.choice(str_column["unique_values"])
#             else:
#                 str_value = "default"  # Default string value
#             query = eval(str(query).replace("<STRVALUE>", f'"{str_value}"', 1))
#             summary = summary.replace("<STRVALUE>", str(str_value), 1)

#     while "<STRVALUE1>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value1 = random.choice(str_column["unique_values"])
#             else:
#                 str_value1 = "default"  # Default string value
#             query = eval(str(query).replace("<STRVALUE1>", f'"{str_value1}"', 1))
#             summary = summary.replace("<STRVALUE1>", str(str_value1), 1)

#     while "<STRVALUE2>" in str(query):
#         if string_fields:
#             str_column = random.choice(string_fields)
#             if str_column["unique_values"]:
#                 str_value2 = random.choice(str_column["unique_values"])
#             else:
#                 str_value2 = "default"  # Default string value
#             query = eval(str(query).replace("<STRVALUE2>", f'"{str_value2}"', 1))
#             summary = summary.replace("<STRVALUE2>", str(str_value2), 1)

#     return query, summary

# import random

# def replace_placeholders(query, summary, fields, string_columns):
#     """
#     Replaces all placeholders in the query and summary with actual column names and values.
#     """
#     # Replace <COLUMN> placeholders
#     while "<COLUMN>" in query:
#         column = random.choice(fields)
#         query = query.replace("<COLUMN>", column["name"])
#         summary = summary.replace("<COLUMN>", column["name"])

#     # Replace <COLUMN1> and <COLUMN2> placeholders
#     while "<COLUMN1>" in query:
#         column1 = random.choice(fields)
#         query = query.replace("<COLUMN1>", column1["name"])
#         summary = summary.replace("<COLUMN1>", column1["name"])

#     while "<COLUMN2>" in query:
#         column2 = random.choice([col for col in fields if col["name"] != column1["name"]])
#         query = query.replace("<COLUMN2>", column2["name"])
#         summary = summary.replace("<COLUMN2>", column2["name"])

#     # Replace <STRVALUE> placeholders
#     while "<STRVALUE>" in query:
#         str_column = random.choice(string_columns)
#         str_value = random.choice(str_column["unique_values"]) if str_column["unique_values"] else "default"
#         query = query.replace("<STRVALUE>", str_value)
#         summary = summary.replace("<STRVALUE>", str_value)

#     # Replace <STRVALUE1> and <STRVALUE2> placeholders
#     while "<STRVALUE1>" in query:
#         str_column1 = random.choice(string_columns)
#         str_value1 = random.choice(str_column1["unique_values"]) if str_column1["unique_values"] else "default"
#         query = query.replace("<STRVALUE1>", str_value1)
#         summary = summary.replace("<STRVALUE1>", str_value1)

#     while "<STRVALUE2>" in query:
#         str_column2 = random.choice(string_columns)
#         str_value2 = random.choice(str_column2["unique_values"]) if str_column2["unique_values"] else "default"
#         query = query.replace("<STRVALUE2>", str_value2)
#         summary = summary.replace("<STRVALUE2>", str_value2)

#     return query, summary

# def generate_mongodb_query(metadata):
#     # Define MongoDB query templates as strings with placeholders
#     templates_with_summaries = [
#         # Simple equality
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": \"<STRVALUE>\"})",
#             "summary": "Find documents where <COLUMN> equals <STRVALUE>."
#         },
#         # $in operator
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"<STRVALUE>\", \"<STRVALUE>\", \"<STRVALUE>\"] }})",
#             "summary": "Find documents where <COLUMN> matches one of the given values."
#         },
#         # $ne operator
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$ne\": \"<STRVALUE>\" }})",
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#         # Logical AND
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN1>\": \"<STRVALUE1>\", \"<COLUMN2>\": \"<STRVALUE2>\"})",
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> equals <STRVALUE2>."
#         },
#         # Logical OR
#         {
#             "query": "db.<TABLE>.find({ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] })",
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
#         },
#         # Combination of $in and equality
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN1>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] }, \"<COLUMN2>\": \"<STRVALUE3>\"})",
#             "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # $in for range filtering (e.g., years in a range)
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"Year_1\", \"Year_2\", \"Year_3\", \"Year_4\"] }})",
#             "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_1 to Year_4)."
#         },
#         # $in with multiple conditions
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] }, \"<COLUMN2>\": \"<STRVALUE3>\"})",
#             "summary": "Find documents where <COLUMN> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # $and with $in
#         {
#             "query": "db.<TABLE>.find({ \"$and\": [{\"<COLUMN1>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] } }, {\"<COLUMN2>\": \"<STRVALUE3>\"}] })",
#             "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
#         },
#         # Logical NOT
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$not\": { \"$eq\": \"<STRVALUE>\" }}})",
#             "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
#         },
#         # Combination of $or and equality
#         {
#             "query": "db.<TABLE>.find({ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] })",
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
#         },
#         # Filtering on multiple conditions
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN1>\": \"<STRVALUE1>\", \"<COLUMN2>\": { \"$in\": [\"<STRVALUE2>\", \"<STRVALUE3>\"] }})",
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
#         },
#         # Range-based filtering with $in
#         {
#             "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"Year_6\", \"Year_7\", \"Year_8\", \"Year_9\", \"Year_12\"] }})",
#             "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_6 to Year_12)."
#         },
#         # Multiple filters with $and and $or
#         {
#             "query": "db.<TABLE>.find({ \"$and\": [{ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] }, {\"<COLUMN3>\": { \"$ne\": \"<STRVALUE3>\" }}] })",
#             "summary": "Find documents where either <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>, and <COLUMN3> does not equal <STRVALUE3>."
#         },
#         # Nested conditions
#         {
#             "query": "db.<TABLE>.find({ \"$and\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": { \"$in\": [\"<STRVALUE2>\", \"<STRVALUE3>\"] }}] })",
#             "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
#         },
#     ]
    
#     # Select a random collection from the metadata
#     # collection_name = random.choice(list(metadata.keys()))
#     collection_name = 'UW_std_person'
#     fields = metadata[collection_name]  # Get field metadata for the selected collection
    
#     # Filter numeric columns (excluding _id and non-numeric fields)
#     numeric_columns = [col for col in fields if col["type"] in ("int", "float", "decimal") and not col["primary_key"]]
#     string_columns = [col for col in fields if "str" in col["type"] or "text" in col["type"]]
    
#     # Choose a query template randomly
#     template_data = random.choice(templates_with_summaries)
    
#     query = template_data["query"]
#     summary = template_data["summary"].replace("<TABLE>", collection_name)

#     # Replace placeholders in the query with actual column names and values
#     query, summary = replace_placeholders(query, summary, fields, string_columns)

#     return query, summary

templates_with_summaries = [
    # Simple equality
    {
        "query": "db.<TABLE>.find({\"<COLUMN>\": \"<STRVALUE>\"})",
        "summary": "Find documents where <COLUMN> equals <STRVALUE>."
    },
    # $in operator
    {
        "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"<STRVALUE>\", \"<STRVALUE>\", \"<STRVALUE>\"] }})",
        "summary": "Find documents where <COLUMN> matches one of the given values."
    },
    # $ne operator
    {
        "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$ne\": \"<STRVALUE>\" }})",
        "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
    },
    # Logical AND
    {
        "query": "db.<TABLE>.find({\"<COLUMN1>\": \"<STRVALUE1>\", \"<COLUMN2>\": \"<STRVALUE2>\"})",
        "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> equals <STRVALUE2>."
    },
    # Logical OR
    {
        "query": "db.<TABLE>.find({ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] })",
        "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
    },
    # Combination of $in and equality
    {
        "query": "db.<TABLE>.find({\"<COLUMN1>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] }, \"<COLUMN2>\": \"<STRVALUE3>\"})",
        "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
    },
    # # $in for range filtering (e.g., years in a range)
    # {
    #     "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"Year_1\", \"Year_2\", \"Year_3\", \"Year_4\"] }})",
    #     "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_1 to Year_4)."
    # },
    # $in with multiple conditions
    {
        "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] }, \"<COLUMN2>\": \"<STRVALUE3>\"})",
        "summary": "Find documents where <COLUMN> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
    },
    # $and with $in
    {
        "query": "db.<TABLE>.find({ \"$and\": [{\"<COLUMN1>\": { \"$in\": [\"<STRVALUE1>\", \"<STRVALUE2>\"] } }, {\"<COLUMN2>\": \"<STRVALUE3>\"}] })",
        "summary": "Find documents where <COLUMN1> matches one of the given values and <COLUMN2> equals <STRVALUE3>."
    },
    # Logical NOT
    {
        "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$not\": { \"$eq\": \"<STRVALUE>\" }}})",
        "summary": "Find documents where <COLUMN> does not equal <STRVALUE>."
    },
    # Combination of $or and equality
    {
        "query": "db.<TABLE>.find({ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] })",
        "summary": "Find documents where <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>."
    },
    # Filtering on multiple conditions
    {
        "query": "db.<TABLE>.find({\"<COLUMN1>\": \"<STRVALUE1>\", \"<COLUMN2>\": { \"$in\": [\"<STRVALUE2>\", \"<STRVALUE3>\"] }})",
        "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
    },
    # # Range-based filtering with $in
    # {
    #     "query": "db.<TABLE>.find({\"<COLUMN>\": { \"$in\": [\"Year_6\", \"Year_7\", \"Year_8\", \"Year_9\", \"Year_12\"] }})",
    #     "summary": "Find documents where <COLUMN> matches one of the specified range values (Year_6 to Year_12)."
    # },
    # Multiple filters with $and and $or
    {
        "query": "db.<TABLE>.find({ \"$and\": [{ \"$or\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": \"<STRVALUE2>\"}] }, {\"<COLUMN3>\": { \"$ne\": \"<STRVALUE3>\" }}] })",
        "summary": "Find documents where either <COLUMN1> equals <STRVALUE1> or <COLUMN2> equals <STRVALUE2>, and <COLUMN3> does not equal <STRVALUE3>."
    },
    # Nested conditions
    {
        "query": "db.<TABLE>.find({ \"$and\": [{\"<COLUMN1>\": \"<STRVALUE1>\"}, {\"<COLUMN2>\": { \"$in\": [\"<STRVALUE2>\", \"<STRVALUE3>\"] }}] })",
        "summary": "Find documents where <COLUMN1> equals <STRVALUE1> and <COLUMN2> matches one of the given values."
    },
]

import random
import ast
import json

def generate_mongodb_query(metadata, templates_with_summaries):
    # Pick a random collection
    collection_name = random.choice(list(metadata.keys()))
    fields = metadata[collection_name]  # Get field metadata for the collection
    
    # Filter numeric columns (excluding _id and non-numeric fields)
    numeric_columns = [col for col in fields if col["type"] in ("int", "float", "decimal") and not col["primary_key"]]
    string_columns = [col for col in fields if "str" in col["type"] or "text" in col["type"]]
    
    # Select templates based on whether there are numeric columns
    if numeric_columns:
        templates = templates_with_summaries
    else:
        templates = [t for t in templates_with_summaries if "<NUMCOLUMN>" not in t["query"]]

    # Pick a random template
    template_data = random.choice(templates)
    query = template_data["query"].replace("<TABLE>", collection_name)
    summary = template_data["summary"].replace("<TABLE>", collection_name)
    
    # Initialize placeholders
    last_used_column = None
    last_used_column1 = None  # For <COLUMN1>
    column_before_operator = None  # Track column before an operator (e.g., for <NUMVALUE> and <STRVALUE>)

    # Replace <NUMCOLUMN> placeholders
    while "<NUMCOLUMN>" in query:
        if not numeric_columns:
            return "Error: No valid numeric columns available in the selected collection.", None
        num_column = random.choice(numeric_columns)
        query = query.replace("<NUMCOLUMN>", num_column["name"])
        summary = summary.replace("<NUMCOLUMN>", num_column["name"])
        last_used_column = num_column  # Track the column for <NUMVALUE>
    
    # Replace <NUMVALUE> placeholders using the last used numeric column
    while "<NUMVALUE>" in query:
        if last_used_column and last_used_column["unique_values"]:
            num_value = random.choice(last_used_column["unique_values"])
        else:
            return "Error: No valid numeric values available for the selected column.", None
        query = query.replace("<NUMVALUE>", str(num_value))
        summary = summary.replace("<NUMVALUE>", str(num_value))

    # Replace <COLUMN1> and <COLUMN2> placeholders (ensure distinct columns)
    while "<COLUMN1>" in query:
        column1 = random.choice(fields)
        query = query.replace("<COLUMN1>", column1["name"])
        summary = summary.replace("<COLUMN1>", column1["name"])
        last_used_column1 = column1  # Track the column for <STRVALUE>
    
    while "<COLUMN2>" in query:
        column2 = random.choice([col for col in fields if col != last_used_column1])
        query = query.replace("<COLUMN2>", column2["name"])
        summary = summary.replace("<COLUMN2>", column2["name"])

    # Replace <COLUMN> placeholders
    while "<COLUMN>" in query:
        column = random.choice(fields)
        query = query.replace("<COLUMN>", column["name"])
        summary = summary.replace("<COLUMN>", column["name"])
        column_before_operator = column  # Track column before the operator

    # Replace <STRVALUE> placeholders one at a time
    while "<STRVALUE>" in query:
        str_columns = [col for col in fields if "char" in col["type"] or "text" in col["type"]]
        if not str_columns:
            return "Error: No valid string columns available in the selected collection.", None
        str_column = random.choice(str_columns)
        if str_column["unique_values"]:
            str_value = random.choice(str_column["unique_values"])
        else:
            str_value = "default"
        str_value = str(str_value)  # Ensure str_value is always a string
        if "LIKE" in query and "%<STRVALUE>%" in query:
            query = query.replace("%<STRVALUE>%", f"%{str_value}%", 1)  # Replace only one instance
            summary = summary.replace("<STRVALUE>", str_value, 1)
        else:
            query = query.replace("<STRVALUE>", f"'{str_value}'", 1)  # Replace only one instance
            summary = summary.replace("<STRVALUE>", str_value, 1)
    
    # Replace <STRVALUE1> and <STRVALUE2> placeholders one at a time
    while "<STRVALUE1>" in query:
        if not string_columns:
            return "Error: No valid string columns available for <STRVALUE1>.", None
        str_column1 = random.choice(string_columns)
        str_value1 = random.choice(str_column1["unique_values"]) if str_column1["unique_values"] else "default"
        query = query.replace("<STRVALUE1>", str_value1)
        summary = summary.replace("<STRVALUE1>", str_value1)
    
    while "<STRVALUE2>" in query:
        if not string_columns:
            return "Error: No valid string columns available for <STRVALUE2>.", None
        str_column2 = random.choice(string_columns)
        str_value2 = random.choice(str_column2["unique_values"]) if str_column2["unique_values"] else "default"
        query = query.replace("<STRVALUE2>", str_value2)
        summary = summary.replace("<STRVALUE2>", str_value2)

    # Replace <STRVALUE3> if necessary
    while "<STRVALUE3>" in query:
        if not string_columns:
            return "Error: No valid string columns available for <STRVALUE3>.", None
        str_column3 = random.choice(string_columns)
        str_value3 = random.choice(str_column3["unique_values"]) if str_column3["unique_values"] else "default"
        query = query.replace("<STRVALUE3>", str_value3)
        summary = summary.replace("<STRVALUE3>", str_value3)

    # Ensure values after operators come from the correct column (both for <NUMVALUE> and <STRVALUE>)
    while "<NUMVALUE>" in query and column_before_operator:
        if column_before_operator and column_before_operator["unique_values"]:
            num_value = random.choice(column_before_operator["unique_values"])
        else:
            return "Error: No valid values available for the selected column.", None
        query = query.replace("<NUMVALUE>", str(num_value))
        summary = summary.replace("<NUMVALUE>", str(num_value))

    while "<STRVALUE>" in query and column_before_operator:
        if column_before_operator and column_before_operator["unique_values"]:
            str_value = random.choice(column_before_operator["unique_values"])
        else:
            return "Error: No valid values available for the selected column.", None
        query = query.replace("<STRVALUE>", str_value)
        summary = summary.replace("<STRVALUE>", str_value)

    # # Convert the final query into a valid format
    # # Check if the query has an aggregate operator, if so convert it to a list (for aggregate queries)
    # if "$group" in query or "$sum" in query or "$avg" in query:  # Simplified check for aggregate query
    #     query_dict = json.loads(query.replace("'", "\""))  # Convert string query to a valid list format (aggregate)
    #     return query_dict, summary  # Return as a list (aggregate query)
    
    # # Otherwise, treat as a find() query and convert it to a dictionary
    # try:
    #     query_dict = json.loads(query.replace("'", "\""))  # Convert string query to a valid dictionary (find)
    #     return query_dict, summary
    # except Exception as e:
    #     return f"Error: Failed to parse query into valid MongoDB format. {e}", None
    
    return query, summary


# Generate and print 5 MongoDB queries
for _ in range(5):
    query, summary = generate_mongodb_query(metadata, templates_with_summaries)
    while query.startswith("Error:"):
        query, summary = generate_mongodb_query(metadata, templates_with_summaries)
    print("\nGenerated Query:")
    print(query)
    print("Summary:")
    print(summary)

from tabulate import tabulate
import pymongo

# Function to validate query execution in MongoDB
def validate_mongo_query(query, collection):
    try:
        # Determine if the query is an aggregate or find query
        if isinstance(query, list):  # Aggregate queries are lists
            cursor = collection.aggregate(query)
        elif isinstance(query, dict):  # Find queries are dictionaries
            cursor = collection.find(query, limit=10)  # Limit results for performance
        else:
            raise TypeError("Invalid query format. Query must be a dictionary for find() or a list for aggregate().")
        
        # Check if results exist
        results = list(cursor)  # Convert cursor to list
        return bool(results), results  # Return True if results exist and the results
    except pymongo.errors.PyMongoError as e:
        print(f"Error executing query: {e}")
        return False, []


# # Execution logic for MongoDB
# keywords = ['yearsInProgram']  # Example keywords

# MongoDB connection
mongo_username = 'mdmolnar'
mongo_password = 'AtM0nG0d1452'
connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'
client = pymongo.MongoClient(connection_string)
db = client["ChatDB"]  # Replace with your database name

# Generate and print 5 MongoDB queries
for _ in range(5):
    while True:
        mongo_query, summary_text = generate_mongodb_query(metadata, templates_with_summaries)
        
        # Choose a random collection for query execution
        collection_name = random.choice(list(metadata.keys()))
        collection = db[collection_name]  # Access the MongoDB collection
        
        # Validate the query
        is_valid, results = validate_mongo_query(mongo_query, collection)
        if not is_valid:
            continue  # Retry if the query is invalid or fails
        
        # # Check if all keywords are present in the query
        # if not all(keyword.lower() in str(mongo_query).lower() for keyword in keywords):
        #     continue  # Retry if the query does not contain all keywords
        
        # If valid and includes all keywords, print and break
        print("\nGenerated Query:")
        print(mongo_query)
        print("Summary:")
        print(summary_text)
        
        # print("\nOutput:")
        # if results:
        #     # Extract field names and tabulate results
        #     field_names = results[0].keys() if isinstance(results[0], dict) else []
        #     print(tabulate(results, headers=field_names, tablefmt="pretty"))
        # else:
        #     print("No results found.")
        # break

        print("\nOutput:")
        if results:
            if isinstance(results[0], dict):  # Check if results are a list of dictionaries
                print(tabulate(results, headers="keys", tablefmt="pretty"))
            else:
                print("Unexpected result format. Results:", results)
        else:
            print("No results found.")
        break
