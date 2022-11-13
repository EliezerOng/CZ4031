import re

import psycopg2
import itertools

TABLES = {'customer': 150000,
          'lineitem': 6001215,
          'nation': 25,
          'orders': 1500000,
          'part': 200000,
          'partsupp': 800000,
          'region': 5,
          'supplier': 10000
          }
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

SCANS = ['Bitmap Heap Scan', 'Bitmap Index Scan',
         'Index-Only Scan', 'Index Scan', 'Seq Scan']

JOINS = ['Hash Join', 'Merge Join', 'Nested Loop']

qep_tree = None


class Node:
    def __init__(self, plan_dict, parent=None):
        self.info = plan_dict
        self.op = plan_dict['Node Type']
        self.cost = plan_dict['Total Cost']
        self.parent = parent
        self.children = self.set_children()
        self.tables = []
        self.trace = None
        self.total_cost = None

    def set_children(self):
        if 'Plans' not in self.info:
            return []
        else:
            plans = self.info.get('Plans')

        nodes_list = []
        for plan in plans:
            child_node = Node(plan, parent=self)
            nodes_list.append(child_node)
        return nodes_list

    def set_trace(self, trace):
        self.trace = trace

    def set_tables(self):
        if 'Relation Name' in self.info:
            self.tables = [self.info['Relation Name']]
        elif 'Alias' in self.info:
            self.tables = [self.info['Alias']]
        elif self.op == 'Bitmap Index Scan':
            if 'Relation Name' in self.parent.info:
                self.tables = [self.parent.info['Relation Name']]
            if 'Alias' in self.parent.info:
                self.tables = [self.parent.info['Alias']]
        else:
            tables = []
            for child in self.children:
                tables.extend(child.tables)
            self.tables = tables


def build_tree(plan):
    cost = 0
    root = Node(plan['Plan'])

    tree = []
    queue = [root]

    while queue:
        parent = queue.pop(0)
        if 'Relation Name' in parent.info:
            relation = parent.info['Relation Name']
        else:
            relation = ""
        if "Scan" in parent.info['Node Type']:
            print(parent.info['Node Type'] + " in " + relation)
            print("Cost of this operation: " + str(parent.cost))
        else:
            print(parent.info['Node Type'])
            print("Cost of this operation: " + str(parent.cost))

        cost += parent.cost

        if parent.children:
            for child in parent.children:
                queue.append(child)
                tree.append((parent.op, child.op))

    root.set_trace(tree)
    # print(root.trace)
    root.total_cost = cost
    # print("Total cost for this plan: " + str(cost))
    return root


def get_settings(params):
    # print("Params =", params)
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

    # cursor.execute("EXPLAIN ANALYZE VERBOSE " + query)
    # qep = cursor.fetchall()

    # print(qep_json[0][0])
    # for line in qep:
    #     print(line)
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
        print('AQP', x, 'total cost =', x.total_cost)

    return aqp_list


def traverse(root: Node, result, indexes):
    if not root.children:
        root.set_tables()
        if 'Index' in root.op:
            index = retrieve_index(root.info)
            indexes.add(index)
        # print("root.op =", root.op, "root.table =", root.tables)
        return result.append((root.tables, root.op, root))

    for child in root.children:
        traverse(child, result, indexes)
        root.set_tables()
        # print("root.op =", root.op, "root.table =", root.tables)
        result.append((root.tables, root.op, root))

    return result


def search(relation, traversal, op_type):
    # print(f"Searching for {op_type} on {relation}")
    i = 0
    for item in traversal:
        table, op, _ = item
        if (op_type == 'scans' and op in SCANS) or (op_type == 'joins' and op in JOINS):
            if table == relation:
                # print(f"Found {table}, {op}")
                return i
        i += 1


def compare(qep: Node, aqp: Node):
    # if qep.total_cost <= aqp.total_cost:
    #     a, b = qep, aqp
    #     print("QEP is more efficient for the following reasons:")
    # else:
    #     print("AQP is more efficient for the following reasons:")
    a, b = qep, aqp

    indexes = set()
    list_a = traverse(a, [], indexes)
    list_b = traverse(b, [], indexes)

    scans_to_explain = set()
    joins_to_explain = set()

    for item in list_a:

        table_a, op_a, node_a = item

        # Compare scans
        if op_a in SCANS:
            idx = search(table_a, list_b, 'scans')  # Search for scan operator on the same table in the costlier plan
            if idx:
                _, _, node_b = list_b.pop(idx)
                if node_a == 'Bitmap Index Scan':
                    add_a = node_a.parent.cost
                else:
                    add_a = 0
                if node_b == 'Bitmap Index Scan':
                    add_b = node_b.parent.cost
                else:
                    add_b = 0
                if node_a.cost + add_a <= node_b.cost + add_b and node_a.op != node_b.op:  # If operator A is less costly than operator B, add to list to be
                    # explained
                    scans_to_explain.add((node_a, node_b))

        # Compare joins
        elif op_a in JOINS:
            idx = search(table_a, list_b, 'joins')
            if idx:
                _, _, node_b = list_b.pop(idx)
                if node_a.cost <= node_b.cost and node_a.op != node_b.op:  # If operator A is less costly than operator B, add to list to be
                    # explained
                    joins_to_explain.add((node_a, node_b))
    print(f"scans to explain = {scans_to_explain}, joins = {joins_to_explain}")
    return scans_to_explain, joins_to_explain, indexes


def retrieve_index(node_info):
    pattern = r"(>)|(<)|(<=)|(>=)"
    if 'Index Name' in node_info:
        relation, idx_key = node_info['Index Name'].split('_')
        print(f"relation = {relation}")

        if 'Index Cond' in node_info:
            inner = node_info['Index Cond'][1:-1]
            inner = re.sub(pattern, "=", inner)
            left, right = inner.split(' = ')
            print(f"left = {left}, right = {right}")
            r1, k1 = left.split('.')
            print(f"r1 = {r1}, k1 = {k1}")
            if '.' in right:
                r2, k2 = right.split('.')
                print(f"r2 = {r2}, k2 = {k2}")
            else:
                r2 = right

            if r1 == relation or relation in r1:
                return left
            elif r2 == relation or relation in r2:
                return right

        elif 'Recheck Cond' in node_info:
            inner = node_info['Recheck Cond'][1:-1]
            inner = re.sub(pattern, "=", inner)
            print(f"inner = {inner}")
            left, right = inner.split(' = ')
            print(f"left = {left}, right = {right}")
            r1, k1 = left.split('.')
            print(f"r1 = {r1}, k1 = {k1}")
            if '.' in right:
                r2, k2 = right.split('.')
                print(f"r2 = {r2}, k2 = {k2}")
            else:
                r2 = right

            if r1 == relation or relation in r1:
                return left
            elif r2 == relation or relation in r2:
                return right
        elif 'Filter' in node_info:
            inner = node_info['Filter'][1:-1]
            inner = re.sub(pattern, "=", inner)
            print(f"inner = {inner}")
            left, right = inner.split(' = ')
            print(f"left = {left}, right = {right}")
            r1, k1 = left.split('.')
            print(f"r1 = {r1}, k1 = {k1}")
            if '.' in right:
                r2, k2 = right.split('.')
                print(f"r2 = {r2}, k2 = {k2}")
            else:
                r2 = right

            if r1 == relation or relation in r1:
                return left
            elif r2 == relation or relation in r2:
                return right
