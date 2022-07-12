from math import ceil
from collections import deque

def parse_line(line):
    ingredients_str, products_str = line.strip().split(' => ')
    prod_n, prod_name = products_str.split()
    prod_n = int(prod_n)

    ingredients = []
    for istr in ingredients_str.split(', '):
        ing_n, ing_name = istr.split()
        ing_n = int(ing_n)
        ingredients.append((ing_n, ing_name))
    return (prod_n, prod_name), ingredients


def parse_input(fname='input.txt'):
    reactions = {}
    with open(fname) as f:
        for line in f:
            products, ingredients = parse_line(line)
            reactions[products] = ingredients

    return reactions

class Node:
    def __init__(self, name, amount=0, needed=0, num_made=1, children=None, parents=None):
        self.name = name
        self.amount = amount
        self.needed = needed
        self.num_made = num_made
        self.children = [] if (children is None) else children
        self.parents = [] if (parents is None) else parents

    def make(self, num=None):
        if num is None:
            num = ceil((self.needed - self.amount)/self.num_made)
        self.amount += num*self.num_made
        for n, child in self.children:
            child.needed += n*num

    def __str__(self):
        return f"{self.name}({self.amount}/{self.needed})"

    def __repr__(self):
        return self.__str__()

def make_tree(reactions):
    nodes = {}
    for products, ingredients in reactions.items():
        num_made, prod_name = products
        if prod_name in nodes:
            node = nodes[prod_name]
        else:
            node = Node(prod_name)
            nodes[prod_name] = node
        node.num_made = num_made
        for ingredient in ingredients:
            n, ing_name = ingredient
            if ing_name in nodes:
                child = nodes[ing_name]
            else:
                child = Node(ing_name)
                nodes[ing_name] = child
            
            node.children.append((n, child))
            child.parents.append(node)
    return nodes

reactions = parse_input('input.txt')
nodes = make_tree(reactions)
fuel = nodes['FUEL']
fuel.needed = 1
tomake = deque([fuel])
while tomake:
    node = tomake.popleft()

    # skip if any of parents still need to be made
    skip = False
    for parent in node.parents:
        if parent in tomake:
            skip = True
            break
    
    if skip:
        tomake.append(node)
    else:
        node.make()
        for n, child in node.children:
            if child not in tomake:
                tomake.append(child)
    
ore = nodes['ORE']
print(f"amount of {ore} = {ore.amount}")