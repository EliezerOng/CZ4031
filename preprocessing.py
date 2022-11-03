import psycopg2

parameters = {

    'enable_async_append' : 'ON',
    'enable_bitmapscan' : 'ON',
    'enable_gathermerge' : 'ON',
    'enable_hashagg' : 'ON',
    'enable_hashjoin' : 'ON',
    'enable_incremental_sort' : 'ON',
    'enable_indexscan' : 'ON',
    'enable_indexonlyscan' : 'ON',
    'enable_indexonlyscan' : 'ON',
    'enable_memoize' : 'ON',
    'enable_mergejoin' : 'ON',
    'enable_nestloop' : 'ON',
    'enable_parallel_append' : 'ON',
    'enable_parallel_hash' : 'ON',
    'enable_partition_pruning' : 'ON',
    'enable_partitionwise_join' : 'ON',
    'enable_partitionwise_join' : 'ON',
    'enable_seqscan' : 'ON',
    'enable_sort' : 'ON',
    'enable_tidscan' : 'ON'

}

#establishing the connection
def connect():

    conn = psycopg2.connect(
    database="TPC-H", user='postgres', password='admin123', host='localhost'
    )

    print("Connecting to sql database...")
    cursor = conn.cursor()
    print("Successfully connected to sql database!")
    return cursor

cursor = connect()
print("Executing SQL query")
cursor.execute("EXPLAIN ANALYSE SELECT * FROM customer")

print("SQL query executed")

cost = cursor.fetchone()
print(cost[0])





