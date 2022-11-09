import psycopg2

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


class Node:
    def __init__(self, plan_dict):
        self.op = plan_dict['Node Type']
        self.cost = plan_dict['Total Cost']
        self.output = plan_dict['Output']
        self.plans = plan_dict['Plans']
        self.children = self.set_children()

    def get_children(self):
        return self.children

    def set_children(self):
        nodes_list = []
        for plan in self.plans:
            child_node = Node(plan)
            nodes_list.append(child_node)
        return nodes_list

    def get_operation(self):
        return self.op

    def get_cost(self):
        return self.cost

    def get_output(self):
        return self.output


def build_tree(plan):
    return Node(plan)


def get_settings(params):
    # print(params)
    settings = ""
    for key, value in params.items():
        default = DEFAULT_PARAMS.get(key)
        if value != default:
            settings += "SET " + key + " = '" + value + "';\n"
    # print("settings =", settings)
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
    cursor.execute("EXPLAIN (FORMAT JSON, ANALYZE, VERBOSE) " + query)

    print("SQL query executed")
    qep_json = cursor.fetchone()

    cursor.execute("EXPLAIN ANALYZE VERBOSE " + query)
    qep = cursor.fetchall()

    print(qep_json[0][0])
    cursor.close()
    return qep, qep_json[0][0]


def get_aqp(params, query):
    cursor = connect()
    print("Executing SQL query (AQP)")
    cursor.execute(get_settings(params) + "EXPLAIN (SETTINGS ON, FORMAT JSON, ANALYZE, VERBOSE) " + query)

    print("SQL query executed")
    aqp_json = cursor.fetchone()

    cursor.execute(get_settings(params) + "EXPLAIN (SETTINGS ON, ANALYZE, VERBOSE) " + query)
    aqp = cursor.fetchall()

    print(aqp_json[0][0])
    cursor.close()
    return aqp, aqp_json[0][0]
