from copy import deepcopy
from collections import defaultdict, deque
from sys import maxsize


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

def clean_maze(maze):
    xs = [coord[0] for coord, value in maze.items() if value == '#']
    ys = [coord[1] for coord, value in maze.items() if value == '#']
    xmin, xmax = min(xs), max(xs)
    ymin, ymax = min(ys), max(ys)

    todel = []
    toadd = []
    maze2 = deepcopy(maze)
    for coord, c in maze2.items():
        if c in '#. ':
            continue
        i, j = coord
        bottom = (i+1, j)
        bbottom = (i+2, j)
        top = (i-1, j)
        ttop = (i-2, j)
        left = (i, j-1)
        lleft = (i, j-2)
        right = (i, j+1)
        rright = (i, j+2)
        if (c2 := maze[bottom]) not in '#. ':  # found top of vertical
            name = c + c2
            newloc = top if maze[top] == '.' else bbottom
            todel.extend([coord, bottom])
        elif (c2 := maze[top]) not in '#. ':  # found bottom of vertical
            name = c2 + c
            newloc = bottom if maze[bottom] == '.' else ttop
            todel.extend([coord, top])
        elif (c2 := maze[right]) not in '#. ':  # found left of horizontal
            name = c + c2
            newloc = left if maze[left] == '.' else rright
            todel.extend([coord, right])
        elif (c2 := maze[left]) not in '#. ':  # found right of horizontal
            name = c2 + c
            newloc = right if maze[right] == '.' else lleft
            todel.extend([coord, left])
        toadd.append((newloc, name))
    for coord in set(todel):
        del maze[coord]
    for coord, name in set(toadd):
        x, y = coord
        if x in (xmin, xmax) or y in (ymin, ymax):
            name += 'out'
        else:
            name += 'in'
        maze[coord] = name
    return maze

def get_nodes(maze):
    return {name: coord for coord, name in maze.items() if name not in '#. '}

def bfs(nodes, startcoord, maze):
    dist = 0
    adjacents = {}
    seen = {startcoord}
    queue = deque([(startcoord, dist)])
    while queue:
        coord, dist = queue.popleft()
        if maze[coord] in nodes and dist > 0:
            adjacents[maze[coord]] = dist
        neighbors = get_neighbors(coord)
        for neighbor in neighbors:
            if ((maze[neighbor] == '.') or (maze[neighbor] in nodes)) and (neighbor not in seen):
                queue.append((neighbor, dist+1))
                seen.add(neighbor)
    return adjacents

def find_matching_portal(nodes, name):
    prefix = name[:2]
    try:
        matching = [newname for newname in nodes if newname.startswith(prefix) and newname != name][0]
    except IndexError:
        return None
    return matching

def make_graph(nodes, maze):
    graph = {}
    for name, coord in nodes.items():
        adjacents = bfs(nodes, coord, maze)
        name2 = find_matching_portal(nodes, name)
        if name2:
            adjacents[name2] = 1
        graph[name] = adjacents
    return graph

def make_graph_recursive(graph, level=0):
    newgraph = {}
    if level:
        for name, adjacents in graph.items():
            base, edge = name[:2], name[2:]
            newadjacents = {}
            for aname, distance in adjacents.items():
                abase, aedge = aname[:2], aname[2:]
                if base == abase:
                    newlevel = level+1 if edge == 'in' else level-1
                else:
                    newlevel = level
                newadjacents[f"{aname}_{newlevel}"] = distance
            newgraph[f"{name}_{level}"] = newadjacents
    else:
        for name, adjacents in graph.items():
            base, edge = name[:2], name[2:]
            if edge == 'in':
                newadjacents = {}
                for aname, distance in adjacents.items():
                    abase, aedge = aname[:2], aname[2:]
                    if abase == base:
                        newadjacents[f"{aname}_{level+1}"] = distance
                    elif aedge == 'in':
                        newadjacents[f"{aname}_{level}"] = distance
                    elif abase in ('AA', 'ZZ'):
                        newadjacents[f"{aname}_{level}"] = distance
                newgraph[f"{name}_{level}"] = newadjacents
        for name in ('AAout', 'ZZout'):
            adjacents = graph[name]
            newadjacents = {}
            for aname, distance in adjacents.items():
                abase, aedge = aname[:2], aname[2:]
                if aedge == 'in':
                    newadjacents[f"{aname}_{level}"] = distance
            newgraph[f"{name}_{level}"] = newadjacents

    return newgraph

def dijkstra(graph, start, end):
    distances = defaultdict(lambda: maxsize)
    distances[start] = 0
    prevs = defaultdict(lambda: None)
    visited = set()
    queue = [(0, start)]
    while queue:
        distance, node = queue.pop()
        visited.add(node)
        if node == end:
            return distances, prevs

        level = int(node.split('_')[1])
        newgraph = make_graph_recursive(graph, level)

        for neighbor, delta in newgraph[node].items():
            if neighbor in visited:
                continue
            newdistance = distance + delta
            if newdistance < distances[neighbor]:
                distances[neighbor] = newdistance
                prevs[neighbor] = node
                queue.append((newdistance, neighbor))
        queue.sort(reverse=True)
    return distances, prevs
    

maze = parse_input('input.txt')
maze = clean_maze(maze)
nodes = get_nodes(maze)
graph = make_graph(nodes, maze)
distances, prevs = dijkstra(graph, 'AAout_0', 'ZZout_0')
print(f"AAout_0 to ZZout_0 = {distances['ZZout_0']}")