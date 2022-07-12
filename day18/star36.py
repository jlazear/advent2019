from copy import deepcopy
from collections import defaultdict, deque
from sys import maxsize
from functools import cache


def get_neighbors(coord):
    i, j = coord
    return [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]

def parse_input(fname='input.txt'):
    maze = defaultdict(lambda: '#')
    with open(fname) as f:
        for i, line in enumerate(f):
            for j, c in enumerate(line.strip('\n')):
                maze[(i, j)] = c

    return maze

def modify_maze(maze):
    nodes = get_nodes(maze)
    center = nodes['@']
    i, j = center
    ul = (i-1, j-1)
    u = (i-1, j)
    ur = (i-1, j+1)
    l = (i, j-1)
    r = (i, j+1)
    dl = (i+1, j-1)
    d = (i+1, j)
    dr = (i+1, j+1)
    for coord in (u, d, r, l, center):
        maze[coord] = '#'
    for i, coord in enumerate((ul, ur, dl, dr)):
        maze[coord] = str(i)
    return maze

def get_nodes(maze):
    return {name: coord for coord, name in maze.items() if name not in '#.'}


def bfs(nodes, startcoord, maze):
    dist = 0
    adjacents = {}
    seen = {startcoord}
    queue = deque([(startcoord, dist)])
    while queue:
        coord, dist = queue.popleft()
        if maze[coord] in nodes and dist > 0:
            adjacents[maze[coord]] = dist
            continue
        neighbors = get_neighbors(coord)
        for neighbor in neighbors:
            if ((maze[neighbor] == '.') or (maze[neighbor] in nodes)) and (neighbor not in seen):
                queue.append((neighbor, dist+1))
                seen.add(neighbor)
    return adjacents

def make_graph(nodes, maze):
    graph = {}
    for name, coord in nodes.items():
        adjacents = bfs(nodes, coord, maze)
        graph[name] = adjacents
    return graph

def freeze_graph(graph):
    fgraph = []
    for name, adjacents in sorted(graph.items()):
        new_adjacents = []
        for aname, distance in sorted(adjacents.items()):
            new_adjacents.append((aname, distance))
        fgraph.append((name, tuple(new_adjacents)))
    return tuple(fgraph)

@cache
def dijkstra_mod(start, keys):
    distances = defaultdict(lambda: maxsize)
    distances[start] = 0
    visited = set()
    queue = [(0, start)]
    accessible = {}
    while queue:
        distance, node = queue.pop()
        visited.add(node)
        if node.islower() and node not in keys:
            accessible[node] = distance
            continue
        if node.isupper() and node.lower() not in keys:
            continue

        for neighbor, delta in graph[node].items():
            if neighbor in visited:
                continue
            newdistance = distance + delta
            if newdistance < distances[neighbor]:
                distances[neighbor] = newdistance
                queue.append((newdistance, neighbor))
        queue.sort(reverse=True)
    return accessible

@cache
def solved(keys):
    allkeys = set([key for key in graph if key.islower()])
    return keys == allkeys

@cache
def solve(poses, keys):
    if solved(keys):
        return 0
    accessible_keys = [dijkstra_mod(pos, keys) for pos in poses]
    newdistances = []
    for i, accessible in enumerate(accessible_keys):
        for next_key, delta in accessible.items():
            newkeys = keys.union({next_key})
            new_poses = list(poses)
            new_poses[i] = next_key
            newdistance = delta + solve(tuple(new_poses), newkeys)
            newdistances.append(newdistance)
    return min(newdistances)

maze = parse_input('input.txt')
maze = modify_maze(maze)
nodes = get_nodes(maze)
graph = make_graph(nodes, maze)
poses0 = ('0', '1', '2', '3')
distance = solve(poses0, frozenset())
print(f"{distance = }")
