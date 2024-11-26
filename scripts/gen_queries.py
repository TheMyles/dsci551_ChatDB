from generate_sql_examples_final import get_mysql_metadata
import numpy as np
from mongo_examples_testing import get_mongodb_metadata
import pymysql
from tabulate import tabulate

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

order_words = ["order by", "sort", "sort by", "ordered", "order", "ascending", "descending", "rank", "arrange", "prioritize",
               "sequence", "order", "hierarchy", "top", "bottom", "sorted", 'biggest', 'smallest']

desc_words = ['descending', 'desc', 'biggest to smallest', 'reverse', 'biggest']
limit_words = ['top', 'bottom', 'highest', 'lowest', 'biggest', 'smallest', 'limit']

def execute_sql_query(user_input, keywords, login_info):
    user_list = user_input.replace(',', '').split()
    
    mdata = get_mysql_metadata(login_info)

    tables = [table for table in mdata.keys()]

    assoc_tables = []

    for word in user_list:
        if word in tables:
            assoc_tables.append(word)
    # print('tables:', assoc_tables)

    assoc_cols = []
    col_idx_mdata = []
    for i in range(len(assoc_tables)):
        table_columns = []
        for j in range(len(mdata[assoc_tables[i]])):
            table_columns.append(mdata[assoc_tables[i]][j]['name'])

        # print('tcols:', table_columns)
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

    if len(assoc_cols) == 0:
        assoc_cols.append('*')
    # print('assoc_cols:', assoc_cols)

    query = ''
    from_in_query = False

    if 'SELECT' in keywords:
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

        # print("WHERE:", processes)

        query += 'WHERE '
        for process_idx in range(0, len(processes), 3):
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

        query = query.replace("SELECT", f"SELECT {col},")
    
    if 'HAVING' in keywords:
        pass
    
    if 'ORDER BY' in keywords:
        asc = 'ASC'
        order = []

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
                bigram = word + f' {user_list[i+1]}'
            except:
                pass
            try:
                trigram = bigram + f' {user_list[i+2]}'
            except:
                pass
            if word in desc_words or bigram in desc_words or trigram in desc_words:
                asc = 'DESC'

        query += f'ORDER BY ' + ', '.join(order) + f' {asc} '
    
    
    if 'LIMIT' in keywords:
        query += 'LIMIT '
        for i, word in enumerate(user_list):
            if word in limit_words:
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

    user_list = user_input.replace(",", "").split()

    sql_mdata = get_mysql_metadata(login_info)
    mongo_mdata = get_mongodb_metadata(login_info)

    for word in user_list:
        if word in sql_mdata.keys():
            decision.append(1)
        elif word in mongo_mdata.keys():
            decision.append(0)

    if np.mean(decision) > 0.5:
        return 'SQL'
    elif len(decision) > 0:
        return'MONGODB'
    else:
        return 'UNDEFINED'
