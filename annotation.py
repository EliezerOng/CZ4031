from preprocessing import *
import json


def parse_query(query):
    query_plan = get_qep(query)
    query_plan = query_plan[2:-2]
    query_plan = json.loads(query_plan)
    return query_plan['Plan']


def query_execution(query):
    query_plan = parse_query(query)
    root_node = build_relation(query_plan)
    build_annotation(root_node)


def build_relation(query):
    root_node = Node(query['Node Type'])

    if query['Plans']:
        root_node.add_children(query['Plans'])

    return root_node


def build_annotation(root_node):
    result = []

    dfs(root_node, result)

    result.append(get_description(root_node))

    print(result)


def dfs(root_node, result):
    if root_node:
        if root_node.children:
            for child in root_node.children:
                dfs(child, result)
                result.append(get_description(child))


def get_description(node):
    tmp_string = ""
    if node.node_type == 'Seq Scan':
        tmp_string = "Perform sequential scan on table {}".format(node.relation_name)
    elif node.node_type == 'Hash':
        tmp_string = "Perform hash on table {}".format(node.children[0].relation_name)
    elif node.node_type == 'Hash Join':
        tmp_string = 'Perform a hash join on tables '
        for child in node.children:
            while child.parent_relationship == 'Inner':
                child = child.children[0]
            tmp_string += "{} ".format(child.relation_name)

    return tmp_string


class Node:
    def __init__(self, node_type):
        self.node_type = node_type
        self.children = []

    def add_children(self, children):
        for plan in children:
            tmp = Node(plan['Node Type'])
            tmp.parent = self
            if 'Relation Name' in plan:
                tmp.relation_name = plan['Relation Name']
            if 'Parent Relationship' in plan:
                tmp.parent_relationship = plan['Parent Relationship']
            self.children.append(tmp)
            if 'Plans' in plan:
                tmp.add_children(plan['Plans'])
