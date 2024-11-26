import pymongo

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

