import re
import preprocessing as pre

WORK_MEM = 4


def build_annotation(root):
    result = []

    final = dfs(root, result)
    result.append(final[1])

    # print(root.info)

    result.append(root.total_cost)

    return result


def dfs(root, result):
    tables = []

    tmp_string = ""

    if root.children:
        for child in root.children:
            tmp = dfs(child, result)
            tables.append(tmp[0])
            result.append(tmp[1])

    if root.op == 'Seq Scan':
        table = root.info['Relation Name']
        alias = root.info['Alias']
        tmp_string = "Perform sequential scan on table {} as {}".format(table, alias)
        return table, tmp_string

    elif root.op == 'Index Scan':
        table = root.info['Relation Name']
        alias = root.info['Alias']
        tmp_string = "Perform index scan on table {} as {} using index on {}".format(table, alias,
                                                                                     root.info['Index Name'])
        if 'Index Cond' in root.info:
            tmp_string += ' where {}'.format(root.info['Index Cond'])
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        return table, tmp_string

    elif root.op == 'Index-Only Scan':
        table = root.info['Relation Name']
        alias = root.info['Alias']
        tmp_string = "Perform index only scan on table {} as {} using index on {}".format(table, alias,
                                                                                          root.info['Index Name'])
        if 'Index Cond' in root.info:
            tmp_string += ' where {}'.format(root.info['Index Cond'])
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        return table, tmp_string

    elif root.op == 'Foreign Scan':
        table = root.info['Relation Name']
        alias = root.info['Alias']
        tmp_string = "Perform foreign scan on table {} from schema {} as {}".format(table, root.info['Schema'], alias)
        return table, tmp_string

    elif root.op == 'Subquery Scan':
        tmp_string = "Perform subquery scan on previous operation"
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        return tables[0], tmp_string

    elif root.op == 'CTE Scan':
        table = root.info['CTE Name']
        alias = root.info['Alias']
        tmp_string = 'Perform CTE scan on table {} as {}'.format(table, alias)
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        return table, tmp_string

    elif root.op == 'Function Scan':
        table = root.info['Schema']
        alias = root.info['Alias']
        tmp_string = 'Perform function {} on schema {} as {}'.format(root.info['Function Name'], table, alias)
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        return table, tmp_string

    elif root.op == 'TID Scan':
        table = root.info['Relation Name']
        alias = root.info['Alias']
        tmp_string = 'Perform TID Scan on table {} as {}'.format(table, alias)
        return table, tmp_string

    elif root.op == 'Hash':
        tmp_string = "Perform hash on table {}".format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'HashAggregate':
        tmp_string = 'Perform hash aggregate operation on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Aggregate':
        tmp_string = 'Perform aggregate on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Append':
        tmp_string = 'Append results from table {} to table {}'.format(tables[0], tables[1])
        return tables[0], tmp_string

    elif root.op == 'Gather':
        tmp_string = 'Perform gather operation on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Gather Merge':
        tmp_string = 'Perform gather merge operation on result of previous operations'
        return tables[0], tmp_string

    elif root.op == 'GroupAggregate':
        tmp_string = 'Perform group aggreagate operation on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Hash Join':
        tmp_string = "Perform hash join on tables {} and {}".format(tables[0], tables[1])
        return tables[0], tmp_string

    elif root.op == 'Nested Loop':
        tmp_string = 'Perform nested loop join on tables {} and {}'.format(tables[0], tables[1])
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        if 'Join Filter' in root.info:
            tmp_string += ' with condition {}, {}, {}'.format(tables[0], tables[1], root.info['Join Filter'])
        return tables[0], tmp_string

    elif root.op == 'Merge Join':
        tmp_string = 'Perform merge join on tables {} and {}'.format(tables[0], tables[1])
        if 'Filter' in root.info:
            tmp_string += ' with filter {}'.format(root.info['Filter'])
        if 'Merge Cond' in root.info:
            tmp_string += ' with condition {}'.format(root.info['Merge Cond'])
        return tables[0], tmp_string

    elif root.op == 'Sort':
        tmp_string = 'Perform sort operation on table {} with sort key {}'.format(tables[0], root.info['Sort Key'])
        return tables[0], tmp_string

    elif root.op == 'Incremental Sort':
        tmp_string = 'Perform incremental sort operation on table {} with sort key {}'.format(tables[0],
                                                                                              root.info['Sort Key'])
        return tables[0], tmp_string

    elif root.op == 'Limit':
        tmp_string = 'Number of rows is limited from table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Materialize':
        tmp_string = 'Perform materialize operation on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'ModifyTable':
        table = root.info['Relation Name']
        tmp_string = 'Modify table {}'.format(table)
        return table, tmp_string

    elif root.op == 'MergeAppend':
        tmp_string = 'Merge results from table {} and {}'.format(tables[0], tables[1])
        return tables[0], tmp_string

    elif root.op == 'SetOp':
        tmp_string = 'Perform set operation on table {}'.format(tables[0])
        return tables[0], tmp_string

    elif root.op == 'Unique':
        table = ''
        if 'Subplan Name' in root.info:
            table = root.info['Subplan Name']
        else:
            table = tables[0]

        tmp_string = 'Remove duplicates from table {}'.format(table)

        return table, tmp_string

    else:
        tmp_string = 'Perform {} operation from table {}'.format(root.op, tables[0])

        return tables[0], tmp_string
    else:
        tmp_string = 'Perform {} operation'.format(root.op)
        return 'Unknown', tmp_string


def build_explanation(qep: pre.Node, aqp: pre.Node):
    scans = []
    joins = []

    if qep.trace == aqp.trace:
        print("Plans do not show significant differences.")
        return scans, joins

    scan_diff, join_diff, indexes = pre.compare(qep, aqp)
    for diff in scan_diff:
        scan_exp = explain_scan(diff[0], diff[1])
        scans.append(scan_exp)
    for diff in join_diff:
        join_exp = explain_joins(diff[0], diff[1], indexes)
        joins.append(join_exp)
    print(f'scans = {scans}, joins = {joins}')
    return scans, joins


def explain_scan(a: pre.Node, b: pre.Node):
    explanation = ""

    # Index scan better than Seq scan
    if a.op == "Index Scan" and b.op == "Seq Scan":
        explanation += f"Index Scan is done on {a.tables} instead of Sequential Scan because the selectivity of " \
                       f"predicate {a.info['Index Cond']} is low. "
        if a.info['Index Name']:
            explanation += f"This is possible due to the {a.info['Index Name']} index. "

    # Seq scan better than other scans
    elif a.op == "Seq Scan" and b.op != "Seq Scan":
        print(f"a.info = {a.info}")
        if 'Filter' in a.info:
            filter_cond = a.info['Filter']
        else:
            filter_cond = ""
        explanation += f"Sequential Scan is done on {a.tables} instead of {b.op} because the selectivity of " \
                       f"predicate {filter_cond} is high. "

        if a.tables == 'region':
            explanation += f"The region table is also small, with only 5 rows. "
        elif a.tables == 'nation':
            explanation += f"the nation table is also small, with only 25 rows. "

    # Bitmap scan better
    elif a.op == "Bitmap Index Scan" and b.op != "Bitmap Index Scan":
        explanation += f"Bitmap Scan is done on {a.tables} instead of {b.op} because the {a.info['Index Name']} index " \
                       f"exists, but the selectivity of predicate {a.info['Index Cond']} is high. "

    # Index-only scan better
    elif a.op == "Index-Only Scan" and b.op != "Index-Only Scan":
        explanation += f"Index-Only Scan is done on {a.tables} instead of {b.op} because the {a.info['Index Name']} index exists "
        if 'Index Cond' in a.info:
            explanation += f"and the column that needs to be fetched by the predicate {a.info['Index Cond']} is the " \
                           f"key of the index. "
        else:
            explanation += f"and the column that needs to be fetched by the predicate is the key of the index. "

    return explanation


def explain_joins(a: pre.Node, b: pre.Node, indexes):
    explanation = ""
    pattern = r'.'

    input1 = a.children[0]
    input2 = a.children[1]
    size1 = input1.info['Plan Rows']
    size2 = input2.info['Plan Rows']

    if a.op == "Nested Loop":
        explanation += f"Nested Loop Join performed after {input1.op} and {input2.op} is a more efficient join than {b.op}. "
        if size1 * 2 < size2:
            explanation += f"One join input is much smaller than the other ({size1} row(s) from {input1.op} < {size2} row(s) from {input2.op}). "
        elif size2 * 2 < size1:
            explanation += f"One join input is much smaller than the other ({size2} row(s) from {input2.op} < {size1} row(s) from {input1.op}). "
        if b.cost // a.cost > 1:
            explanation += f"{b.op} costs approximately {b.cost // a.cost} times more than Nested Loop Join. "

    if a.op == "Hash Join":
        explanation += f"Hash Join performed after {input1.op} and {input2.op} is a more efficient join than {b.op}. "
        to_replace = r"(>)|(<)|(<=)|(>=)"
        inner = re.sub(to_replace, "=", a.info['Hash Cond'][1:-1])
        left, right = inner.split(' = ')
        print(f"In Hash Join explain: left = {left}, right = {right}, indexes = {indexes}")
        if left not in indexes and right not in indexes:
            explanation += f"This is because both inputs are not sorted by the join keys in predicate {a.info['Hash Cond']}. "
        if (size1 or size2) > 1000:
            explanation += 'Its inputs are large - '
            if size1 > 1000:
                explanation += f"the output of {input1.op} is estimated to be {size1} rows "
            if size2 > 1000:
                explanation += f"and the output of {input2.op} is estimated to be {size2} rows. "
        if input1.op == "Hash" and 'Peak Memory Usage' in input1.info and input1.info['Peak Memory Usage'] < WORK_MEM:
            explanation += f"The hash table from {input1.op} has peak memory usage of {input1.info['Peak Memory Usage']}, which fits into the buffer of size {WORK_MEM}. "
        elif input2.op == "Hash" and 'Peak Memory Usage' in input2.info and input2.info['Peak Memory Usage'] < WORK_MEM:
            explanation += f"The hash table from {input2.op} has peak memory usage of {input2.info['Peak Memory Usage']}, which fits into the buffer of size {WORK_MEM}. "

    if a.op == "Merge Join":
        mod_string = re.sub(pattern, ' ', a.info['Merge Cond'])
        split_str = mod_string.split()
        inputs = []
        for split in split_str:
            if split.isalnum():
                inputs.append(split)

        explanation += f"Merge Join performed on {inputs[0]} and {inputs[1]} is a more efficient join than {b.op} because both input relations are sorted. "

    return explanation
