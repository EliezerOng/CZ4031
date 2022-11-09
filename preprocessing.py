import psycopg2
import itertools

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

qep_tree = None


class Node:
    def __init__(self, plan_dict):
        self.info = plan_dict
        self.op = plan_dict['Node Type']
        self.cost = plan_dict['Total Cost']
        self.output = self.set_output()
        self.children = self.set_children()
        self.trace = None  # For root nodes only. Returns a dictionary of the whole 'tree'

    def set_children(self):
        if 'Plans' not in self.info:
            return None
        else:
            plans = self.info.get('Plans')

        nodes_list = []
        for plan in plans:
            child_node = Node(plan)
            nodes_list.append(child_node)
        return nodes_list

    def set_output(self):
        if 'Output' not in self.info:
            return None
        else:
            return self.info.get('Output')

    def set_trace(self, trace):
        self.trace = trace


def build_tree(plan):
    root = Node(plan['Plan'])

    tree = []
    queue = [root]

    while queue:
        parent = queue.pop(0)
        if parent.children:
            for child in parent.children:
                queue.append(child)
                tree.append((parent.op, child.op))

    root.set_trace(tree)
    print(root.trace)

    return root


def get_settings(params):
    print("Params =", params)
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
    print("Executing SQL query (QEP):")
    cursor.execute("EXPLAIN (FORMAT JSON, ANALYZE, VERBOSE) " + query)

    print("SQL query executed")
    qep_json = cursor.fetchone()
    qep_root = build_tree(qep_json[0][0])

    cursor.execute("EXPLAIN ANALYZE VERBOSE " + query)
    qep = cursor.fetchall()

    # print(qep_json[0][0])
    for line in qep:
        print(line)
    cursor.close()

    global qep_tree
    qep_tree = qep_root

    return qep_root


def get_aqp(params, query):
    cursor = connect()
    print("Executing SQL query (AQP)")
    cursor.execute(get_settings(params) + "EXPLAIN (SETTINGS ON, FORMAT JSON, ANALYZE, VERBOSE) " + query)

    print("SQL query executed")
    aqp_json = cursor.fetchone()
    aqp_root = build_tree(aqp_json[0][0])

    # cursor.execute(get_settings(params) + "EXPLAIN (SETTINGS ON, ANALYZE, VERBOSE) " + query)
    # aqp = cursor.fetchall()

    # print(aqp_json[0][0])
    # for line in aqp:
    #     print(line)
    cursor.close()
    return aqp_root


def equivalent(a: Node, b: Node):
    return a.trace == b.trace


def is_distinct(aqp_list, alt: Node):
    for aqp in aqp_list:
        if equivalent(aqp, alt):
            return False
    print(alt, "is DISTINCT")
    return True


def get_multi_aqps(params, query):
    count = 0
    for value in params.values():
        if value == "ON":
            count += 1

    permutations = list(itertools.product(["ON", "OFF"], repeat=count))

    aqp_list = [qep_tree]

    for p in permutations:
        i = 0
        alt_params = DEFAULT_PARAMS.copy()
        for key, value in params.items():
            if value == "ON":
                alt_params.update({key: p[i]})
                i += 1
            if i == count:
                print("i =", i, "count =", count)
                break

        alt = get_aqp(alt_params, query)
        if is_distinct(aqp_list, alt):
            aqp_list.append(alt)

    aqp_list.pop(0)

    print("========== aqp_list (", len(aqp_list), ") ==========")
    for x in aqp_list:
        print(x)

    return aqp_list
