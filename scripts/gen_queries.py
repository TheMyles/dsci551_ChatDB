from generate_sql_examples_final import get_mysql_metadata
import numpy as np
from mongo_examples_testing import get_mongodb_metadata
import pymysql
from tabulate import tabulate
import string
import pymongo

aggregate_words = {
    'MIN': ['minimum', 'smallest', 'lowest', 'least', 'min'],
    'MAX': ['maximum', 'largest', 'highest', 'greatest', 'max'],
    'AVG': ['average', 'mean', 'avg'],
    'COUNT': ['count', 'number', 'total', 'many'],
    'SUM': ['sum', 'total', 'add', 'combined']
}

group_words = ["group by", "aggregate", "group", "grouping", "each", "total", "categorize",
                 "partition", "classify", "segment", "cluster", "bucket", 'grouped']

where_words = {
    'LESS_THAN': ['less', 'fewer', 'below', 'under', 'lower than', 
                  'smaller than', 'not exceeding', 'underneath', '<'],
    'GREATER_THAN': ['more', 'greater', 'above', 'over', 'higher than', 
                     'exceeds', 'bigger than', 'larger than', '>'],
    'EQUAL_TO': ['equal', 'exactly', 'equals', 'same as', '=',
                 'identical to', 'matches', 'equivalent to', 'is'],
    'NOT_EQUAL_TO': ['not equal', 'different', 'not the same as', 
                     'does not equal', 'unequal', 'not identical', '!=']
}

order_words = ["order by", "sort", "sort by", "ordered", "order", "rank", "arrange", "prioritize",
               "sequence", "order", "hierarchy", "top", "bottom", "sorted", 'biggest', 'smallest']

desc_words = ['descending', 'desc', 'biggest to smallest', 'reverse', 'biggest']
limit_words = ['top', 'bottom', 'highest', 'lowest', 'biggest', 'smallest', 'limit', 'only']

all_cols = ['all columns', 'every column', 'each column', 'all the columns', 'all of the columns']


def execute_sql_query(user_input, keywords, login_info):
    exclude = string.punctuation.translate(str.maketrans('', '', "_()"))
    user_list = user_input.translate(str.maketrans('', '', exclude)).split()
    
    mdata = get_mysql_metadata(login_info)

    tables = [table for table in mdata.keys()]

    assoc_tables = []

    for word in user_list:
        if word in tables:
            assoc_tables.append(word)
    print('Generating query for table:', assoc_tables)

    assoc_cols = []
    col_idx_mdata = []
    for i in range(len(assoc_tables)):
        table_columns = []
        for j in range(len(mdata[assoc_tables[i]])):
            table_columns.append(mdata[assoc_tables[i]][j]['name'])

        print('Columns in associated table:', table_columns)
        for word in user_list:
            if word in table_columns:
                assoc_cols.append(word)
                idx = table_columns.index(word)
                col_idx_mdata.append(idx)

    unique_vals = []
    for i in assoc_tables:
        for j in col_idx_mdata:
            unique_vals += mdata[i][j]['unique_values']

    unique_vals = [str(item) if isinstance(item, (int, float)) else item for item in unique_vals]

    for i, word in enumerate(user_list):
        try:
            bigram = word + f' {user_list[i+1]}'
        except:
            pass
        try:
            trigram = bigram + f' {user_list[i+2]}'
        except:
            pass
        try:
            quad = trigram + f' {user_list[i+3]}'
        except:
            pass
        if bigram in all_cols or trigram in all_cols or quad in all_cols:
            assoc_cols.append('*')
    if len(assoc_cols) == 0:
        assoc_cols.append('*')
    print('Creating query with columns:', assoc_cols)

    query = ''
    from_in_query = False

    if 'SELECT' in keywords:
        if '*' in assoc_cols:
            query += 'SELECT * '
        else:
            query += 'SELECT ' + ', '.join(assoc_cols) + ' '
    
    elif 'AGGREGATE' in keywords:
        processes = []

        for key, value in aggregate_words.items():
            for i, word in enumerate(user_list):
                if word.lower() in value:
                    processes.append(key)
                    if user_list[i+1] in assoc_cols:
                        processes.append(user_list[i+1])
                    elif user_list[i+2] in assoc_cols:
                        processes.append(user_list[i+2])
        print('AGG:', processes)

        if len(processes)%2 ==1:
            processes.append('*')
        
        query += 'SELECT '

        for key, values in aggregate_words.items():
            if key in processes:
                idx = processes.index(key)

                if idx == len(processes)-2:
                    query += f'{key}({processes[idx+1]})'
                else:
                    query += f'{key}({processes[idx+1]}), '
                assoc_cols.append(f'{key}({processes[idx+1]})')

        query += ' '

    if not from_in_query:
        query += 'FROM ' + ', '.join(assoc_tables) + ' '
        from_in_query = True

    if 'JOIN' in keywords:
        pass

    if 'WHERE' in keywords:
        processes = []

        for key, values in where_words.items():
            for i, word in enumerate(user_list):
                if i < len(user_list)-1:
                    bigram = word + ' ' + user_list[i+1]
                else:
                    bigram = word
        
                if word.lower() in values:
                    if user_list[i-1] in assoc_cols:
                        processes.append(user_list[i-1])
                    elif user_list[i-2] in assoc_cols:
                        processes.append(user_list[i-2])
                    processes.append(key)
                    if user_list[i+1] in unique_vals:
                        processes.append(user_list[i+1])
                    elif user_list[i+2] in unique_vals:
                        processes.append(user_list[i+2])
                    elif f'{user_list[i+1]} {user_list[i+2]}' in unique_vals:
                        processes.append(f'{user_list[i+1]} {user_list[i+2]}')
                    elif f'{user_list[i+2]} {user_list[i+3]}' in unique_vals:
                        processes.append(f'{user_list[i+2]} {user_list[i+3]}')
                                       
                elif bigram.lower() in values:
                    if user_list[i-1] in assoc_cols:
                        processes.append(user_list[i-1])
                    elif user_list[i-2] in assoc_cols:
                        processes.append(user_list[i-2])
                    processes.append(key)
                    if user_list[i+2] in unique_vals:
                        processes.append(user_list[i+2])
                    elif user_list[i+3] in unique_vals:
                        processes.append(user_list[i+3])
                    elif f'{user_list[i+2]} {user_list[i+3]}' in unique_vals:
                        processes.append(f'{user_list[i+2]} {user_list[i+3]}')
                    elif f'{user_list[i+3]} {user_list[i+4]}' in unique_vals:
                        processes.append(f'{user_list[i+3]} {user_list[i+4]}')

        query += 'WHERE '
        if len(processes) > 3:
            for idx in range(1, len(processes)//3):
                processes.insert(idx*3, 'AND')
        
        print("WHERE:", processes)

        for process_idx in range(0, len(processes), 4):
            try:
                processes[process_idx+2] = int(processes[process_idx+2])
                if processes[process_idx+1] == 'GREATER_THAN':
                    query += f'{processes[process_idx]} > {processes[process_idx+2]}'
                elif processes[process_idx+1] == 'LESS_THAN':
                    query += f'{processes[process_idx]} < {processes[process_idx+2]}'
                elif processes[process_idx+1] == 'EQUAL_TO':
                    query += f'{processes[process_idx]} = {processes[process_idx+2]}'
                elif processes[process_idx+1] == 'NOT_EQUAL_TO':
                    query += f'{processes[process_idx]} != {processes[process_idx+2]}'
            except:
                if processes[process_idx+1] == 'GREATER_THAN':
                    query += f'{processes[process_idx]} > {processes[process_idx+2]}'
                elif processes[process_idx+1] == 'LESS_THAN':
                    query += f'{processes[process_idx]} < {processes[process_idx+2]}'
                elif processes[process_idx+1] == 'EQUAL_TO':
                    query += f"{processes[process_idx]} = \'{processes[process_idx+2]}\'"
                elif processes[process_idx+1] == 'NOT_EQUAL_TO':
                    query += f"{processes[process_idx]} != \'{processes[process_idx+2]}\'"
            try:
                if processes[process_idx+3] == 'AND':
                    query += ' AND '
            except:
                pass

        query += ' '

    if 'GROUP BY' in keywords:
        group_by = []

        # for value in group_words:
        for i, word in enumerate(user_list):
            try:
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            if bigram in group_words:
                if user_list[i+1] in assoc_cols:
                    group_by.append(user_list[i+1])
                elif user_list[i+2] in assoc_cols:
                    group_by.append(user_list[i+2])
                elif user_list[i+3] in assoc_cols:
                    group_by.append(user_list[i+3])
            elif word in group_words:
                if user_list[i+1] in assoc_cols:
                    group_by.append(user_list[i+1])
                elif user_list[i+2] in assoc_cols:
                    group_by.append(user_list[i+2])
                elif user_list[i+3] in assoc_cols:
                    group_by.append(user_list[i+3])

        for i, col in enumerate(group_by):
            if i == 0:
                query += f'GROUP BY {col}'
            else:
                query += f', {col}'
        query += ' '
        query = query.replace("SELECT", f"SELECT {col},")
    
    if 'HAVING' in keywords:
        pass
    
    if 'ORDER BY' in keywords:
        asc = 'ASC'
        order = []
        print('ob:', assoc_cols)

        for i, word in enumerate(user_list):
            try:
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            if bigram in order_words:
                if user_list[i+2] in assoc_cols:
                    order.append(user_list[i+2])
                elif user_list[i+3] in assoc_cols:
                    order.append(user_list[i+3])
            elif word in order_words:
                if user_list[i+1] in assoc_cols:
                    order.append(user_list[i+1])
                elif user_list[i+2] in assoc_cols:
                    order.append(user_list[i+2])
                elif user_list[i+3] in assoc_cols:
                    order.append(user_list[i+3])
                
        for i, word in enumerate(user_list):
            try:
                bigram = word.lower() + f' {user_list[i+1]}'.lower()
            except:
                pass
            try:
                trigram = bigram + f' {user_list[i+2]}'
            except:
                pass
            if word.lower() in desc_words or bigram in desc_words or trigram in desc_words:
                asc = 'DESC'

        query += f'ORDER BY ' + ', '.join(order) + f' {asc} '
    
    
    if 'LIMIT' in keywords:
        query += 'LIMIT '
        for i, word in enumerate(user_list):
            if word.lower() in limit_words:
                try:
                    query += f'{int(user_list[i+1])}'
                except:
                    pass
                try:
                    query += f'{int(user_list[i+2])}'
                except:
                    pass
                try:
                    query += f'{int(user_list[i+3])}'
                except:
                    pass
                try:
                    query += f'{int(user_list[i-1])}'
                except:
                    pass
                
    query += ';'
    
    connection = pymysql.connect(
        host = login_info['endpoint'],
        user = login_info['username'],
        password = login_info['password'],
        database = login_info['sql_database_name']
    )

    cursor = connection.cursor()
    print("Executing query:", query)
    try:
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()

        print(tabulate(rows, headers=columns, tablefmt="pretty"))

        cursor.close()
        connection.close()
    except:
        print('Error executing query')

    return


def sql_or_nosql(user_input, login_info):
    decision = []

    user_list = user_input.translate(str.maketrans('', '', string.punctuation.replace('_', ''))).split()

    sql_mdata = get_mysql_metadata(login_info)
    mongo_mdata = get_mongodb_metadata(login_info)

    for word in user_list:
        if word in sql_mdata.keys():
            decision.append(1)
        elif word in mongo_mdata.keys():
            decision.append(0)

    if len(decision) > 0 and np.mean(decision) > 0.5:
        return 'SQL'
    elif len(decision) > 0:
        return'MONGODB'
    else:
        return 'UNDEFINED'


def execute_mongo_query(user_input, keywords, login_info):
    exclude = string.punctuation.translate(str.maketrans('', '', "_()"))
    user_list = user_input.translate(str.maketrans('', '', exclude)).split()

    # Connect to MongoDB
    # connection_string = f'mongodb+srv://{login_info['mongo_username']}:{login_info['mongo_password']}@cluster0.tgu2d.mongodb.net/'
        # MongoDB credentials and connection string
    mongo_username = login_info['mongo_username']
    mongo_password = login_info['mongo_password']
    database_name = login_info['mongo_database_name']

    connection_string = f'mongodb+srv://{mongo_username}:{mongo_password}@cluster0.tgu2d.mongodb.net/'

    mdata = get_mongodb_metadata(login_info)
    client = pymongo.MongoClient(connection_string)
    db = client[login_info['mongo_database_name']]

    collections = db.list_collection_names()

    assoc_collections = [word for word in user_list if word in collections]
    if not assoc_collections:
        print("No matching collections found.")
        return
    print('Generating query for table(s):', assoc_collections)

    assoc_cols = []
    col_idx_mdata = []
    for i in range(len(assoc_collections)):
        table_columns = []
        for j in range(len(mdata[assoc_collections[i]])):
            table_columns.append(mdata[assoc_collections[i]][j]['name'])

        print('Columns in associated table:', table_columns)
        for word in user_list:
            if word in table_columns:
                assoc_cols.append(word)
                idx = table_columns.index(word)
                col_idx_mdata.append(idx)

    unique_vals = []
    for i in assoc_collections:
        for j in col_idx_mdata:
            unique_vals += mdata[i][j]['unique_values']

    print('Creating query with columns:', assoc_cols)

    unique_vals = [str(item) if isinstance(item, (int, float)) else item for item in unique_vals]

    collection = db[assoc_collections[0]]

    pipeline = []
    # Handle WHERE conditions (filters)
    if 'WHERE' in keywords:
        match_stage = {}
        for key, values in where_words.items():
            for i, word in enumerate(user_list):
                try:
                    bigram = word + f' {user_list[i+1]}'
                except:
                    pass
                if word.lower() in values:
                    if user_list[i-1] in assoc_cols:
                        field = user_list[i - 1]
                    elif user_list[i-2] in assoc_cols:
                        field = user_list[i - 2]
                    if user_list[i+1] in unique_vals:
                        value = user_list[i + 1]
                    elif user_list[i+2] in unique_vals:
                        value = user_list[i + 2]
                    elif user_list[i+3] in unique_vals:
                        value = user_list[i + 3]
                    elif f'{user_list[i+1]} {user_list[i+2]}' in unique_vals:
                        value = f'{user_list[i+1]} {user_list[i+2]}'
                    elif f'{user_list[i+2]} {user_list[i+3]}' in unique_vals:
                        value = f'{user_list[i+2]} {user_list[i+3]}'
                    else:
                        value = 100
                    if key == 'LESS_THAN':
                        match_stage[field] = {"$lt": value}
                    elif key == 'GREATER_THAN':
                        match_stage[field] = {"$gt": value}
                    elif key == 'EQUAL_TO':
                        match_stage[field] = value
                    elif key == 'NOT_EQUAL_TO':
                        match_stage[field] = {"$ne": value}
        if match_stage:
            pipeline.append({"$match": match_stage})
    
    if 'SELECT' in keywords or 'AGGREGATE' in keywords:
        for i, word in enumerate(user_list):
            try:
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            try:
                trigram = bigram + f' {user_list[i+2]}'
            except:
                pass
            try:
                quad = trigram + f' {user_list[i+3]}'
            except:
                pass
            if bigram in all_cols or trigram in all_cols or quad in all_cols:
                projection = {"_id": 0}
                break
            elif assoc_cols:
                projection = {col: 1 for col in assoc_cols}
        pipeline.append({"$project": projection})   

    # Handle GROUP BY
    if 'GROUP BY' in keywords:
        group_by_field = None
        for i, word in enumerate(user_list):
            try:
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            if bigram in group_words:
                if user_list[i+1] in assoc_cols:
                    group_by_field = user_list[i+1]
                elif user_list[i+2] in assoc_cols:
                    group_by_field = user_list[i+2]
                elif user_list[i+3] in assoc_cols:
                    group_by_field = user_list[i+3]
            elif word in group_words:
                if user_list[i+1] in assoc_cols:
                    group_by_field = user_list[i+1]
                elif user_list[i+2] in assoc_cols:
                    group_by_field = user_list[i+2]
                elif user_list[i+3] in assoc_cols:
                    group_by_field = user_list[i+3]
        # print("GB:", group_by_field)
        processes = []

        if 'AGGREGATE' in keywords:
            for key, values in aggregate_words.items():
                for i, word in enumerate(user_list):
                    if word.lower() in values:
                        processes.append(key)
                        if user_list[i+1] in assoc_cols:
                            processes.append(f'${user_list[i+1]}')
                        elif user_list[i+2] in assoc_cols:
                            processes.append(f'${user_list[i+2]}')

        group_stage = {
            "$group": {
                "_id": f"${group_by_field}"
            }
        }

        processes = ['SUM' if item == 'COUNT' else item for item in processes]
        if len(processes) % 2 == 1:
            processes.append(1)
        print("AGG:", processes)

        for i, item in enumerate(processes):
            if item in aggregate_words.keys():
                try:
                    alias = f"{item.lower()}_{processes[i+1].replace('$', '')}"
                except:
                    alias = f'{item.lower()}_{processes[i+1]}'
                try:
                    int(processes[i+1])
                    group_stage['$group'][alias] = {f'${item.lower()}': processes[i+1]}
                except:
                    group_stage['$group'][alias] = {f'${item.lower()}': f'{processes[i+1]}'}

        pipeline.append(group_stage)
        if not any('$project' in stage for stage in pipeline):
            pipeline = [stage for stage in pipeline if '$project' not in stage]
    
    elif 'AGGREGATE' in keywords:
        processes = []

        for key, value in aggregate_words.items():
            for i, word in enumerate(user_list):
                if word.lower() in value:
                    processes.append(key)
                    if user_list[i+1] in assoc_cols:
                        processes.append(user_list[i+1])
                    elif user_list[i+2] in assoc_cols:
                        processes.append(user_list[i+2])
        
        processes = ['SUM' if item == 'COUNT' else item for item in processes]
        group_stage = {
            "$group": {
                "_id": None
            }
        }
        if len(processes) % 2 == 1:
            processes.append(1)
        print("AGG:", processes)

        for i, item in enumerate(processes):
            if item in aggregate_words.keys():
                alias = f'{item.lower()}_{processes[i+1]}'
                group_stage['$group'][alias] = {f'${item.lower()}': f'${processes[i+1]}'}

        pipeline.append(group_stage)
        if not any('$project' in stage for stage in pipeline):
            pipeline = [stage for stage in pipeline if '$project' not in stage]

    # Handle ORDER BY
    if 'ORDER BY' in keywords:
        sort_order = 1  # Default to ascending
        for i, word in enumerate(user_list):
            try:
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            if word in desc_words or bigram in desc_words:
                sort_order = -1
            if bigram in order_words:
                if user_list[i+2] in assoc_cols:
                    sort_field = user_list[i+2]
                elif user_list[i+3] in assoc_cols:
                    sort_field = user_list[i+3]
            elif word in order_words:
                if user_list[i+1] in assoc_cols:
                    sort_field = user_list[i+1]
                elif user_list[i+2] in assoc_cols:
                    sort_field = user_list[i+2]
                elif user_list[i+3] in assoc_cols:
                    sort_field = user_list[i+3]

        pipeline.append({"$sort": {sort_field: sort_order}})
    
    # Handle LIMIT
    if 'LIMIT' in keywords:
        for i, word in enumerate(user_list):
            if word in limit_words:
                try:
                    pipeline.append({"$limit": int(user_list[i+1])})
                except:
                    pass
                try:
                    pipeline.append({"$limit": int(user_list[i+2])})
                except:
                    pass
                try:
                    pipeline.append({"$limit": int(user_list[i+3])})
                except:
                    pass
                try:
                    pipeline.append({"$limit": int(user_list[i-1])})
                except:
                    if not any([True for stage in pipeline if '$limit' in stage]):
                        pipeline.append({"$limit": 5})
                
    print("Executing MongoDB pipeline:", pipeline)
    try:
        result = list(collection.aggregate(pipeline))
        headers = result[0].keys()
        data = [row.values() for row in result]
        print(tabulate(data, headers=headers, tablefmt="pretty"))
    except Exception as e:
        print("Error executing query:", e)

    client.close()
