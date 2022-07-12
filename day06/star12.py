class Node:
    def __init__(self, name, parent=None, children=None, depth=None):
        self.name = name
        self.parent = parent
        if children:
            self.children = children
        else:
            self.children = []
        self.depth = depth
    
    def __str__(self):
        children = ','.join([node.name for node in self.children])
        return f"{self.name}({children})"

    def __repr__(self):
        return self.__str__()

def add_orbit(parent, child, nodes):
    if parent in nodes:
        parent_node = nodes[parent]
    else:
        parent_node = Node(parent)
        nodes[parent] = parent_node
    if child in nodes:
        child_node = nodes[child]
    else:
        child_node = Node(child)
        nodes[child] = child_node
    
    parent_node.children.append(child_node)
    child_node.parent = parent_node
    return nodes

def find_path_to_root(node):
    path = [node]
    while node.parent:
        node = node.parent
        path.append(node)
    return path


def find_root(nodes):
    node = nodes[list(nodes.keys())[0]]
    while node.parent:
        node = node.parent
    return node

def assign_depths(node, depth=0):
    node.depth = depth
    for newnode in node.children:
        assign_depths(newnode, depth+1)

def parse_input(fname='input.txt'):
    nodes = {}
    with open(fname) as f:
        for line in f:
            parent, child = line.strip().split(')')
            nodes = add_orbit(parent, child, nodes)
    root = find_root(nodes)
    assign_depths(root)
    return nodes

nodes = parse_input('input.txt')

path_you = find_path_to_root(nodes['YOU'])
path_san = find_path_to_root(nodes['SAN'])
common = set(path_you) & set(path_san)

n_transfers = len(path_you) + len(path_san) - 2*len(common) - 2
print(f"{n_transfers = }")