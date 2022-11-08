import psycopg2
import json

DEFAULT_PARAMS = {

    'enable_async_append': 'ON',
    'enable_bitmapscan': 'ON',
    'enable_gathermerge': 'ON',
    'enable_hashagg': 'ON',
    'enable_hashjoin': 'ON',
    'enable_incremental_sort': 'ON',
    'enable_indexscan': 'ON',
    'enable_indexonlyscan': 'ON',
    'enable_material': 'ON',
    'enable_memoize': 'ON',
    'enable_mergejoin': 'ON',
    'enable_nestloop': 'ON',
    'enable_parallel_append': 'ON',
    'enable_parallel_hash': 'ON',
    'enable_partition_pruning': 'ON',
    'enable_partitionwise_join': 'OFF',
    'enable_partitionwise_aggregate': 'OFF',
    'enable_seqscan': 'ON',
    'enable_sort': 'ON',
    'enable_tidscan': 'ON'

}


def get_settings(params):
    settings = ""
    for key, value in params.items():
        default = DEFAULT_PARAMS.get(key)
        if value != default:
            settings += "SET " + key + " = '" + value + "';\n"
    # param_str += "SELECT name, setting FROM pg_settings WHERE name LIKE '%enable%';"
    return settings


# establishing the connection
def connect():
    conn = psycopg2.connect(
        database="TPC-H", user='postgres', password='admin123', host='localhost'
    )

    print("Connecting to sql database...")
    cursor = conn.cursor()
    print("Successfully connected to sql database!")
    return cursor


def get_qep(query):
    cursor = connect()
    print("Executing SQL query (QEP):", query)
    cursor.execute("EXPLAIN (FORMAT JSON, ANALYZE) " + query)

    print("SQL query executed")

    qep = cursor.fetchall()
    print(qep)
    cursor.close()
    return json.dumps(qep)


def get_aqp(params, query):
    cursor = connect()
    print("Executing SQL query (AQP)")
    cursor.execute(get_settings(params) + "EXPLAIN ANALYZE SETTINGS FORMAT JSON " + query)

    print("SQL query executed")

    aqp = cursor.fetchall()
    print(aqp)
    cursor.close()
    return json.dumps(aqp)
