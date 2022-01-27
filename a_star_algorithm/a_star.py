from ast import For


graph = {
    'A': [('B', 4), ('C', 3)],
    'B': [('F', 5), ('E', 12)],
    'C': [('D', 7), ('E', 10)],
    'D': [('E', 2)],
    'F': [('Z', 16)],
    'E': [('Z', 5)]
}

heuristic = {
    'A': 14,
    'B': 12,
    'C': 11,
    'D': 6,
    'F': 11,
    'E': 4,
    'Z': 1,
}

start = 'A'
stop = 'Z'

# Sets to keep track of visited nodes and adjacent unvisited ones
visit_list = set([start])
done_list = set([])

distance = {}
distance[start] = 0

parent = {}
parent[start] = start


def generateOutput(node):
    result = []

    while parent[node] != node:
        result.append(node)
        node = parent[node]

    result.append(start)

    result.reverse()

    return result


def selectLowestF(node):
    # select node with lowest f(n)
    for v in visit_list:
        if node == None or distance[v] + heuristic[v] < distance[node] + heuristic[node]:
            node = v
    return node


def addToVisitList(m, weight, node):
    visit_list.add(m)
    parent[m] = node
    distance[m] = distance[node] + weight


def changeNodePath(m, weight, node):
    if distance[m] > distance[node] + weight:
        distance[m] = distance[node] + weight
        parent[m] = node

        if m in done_list:
            done_list.remove(m)
            visit_list.add(m)


def a_star_algorithm():
    while len(visit_list) > 0:
        node = None
        node = selectLowestF(node)

        if node == None:
            print(f"There is no path from {start} to {stop}")
            return None

        if node == stop:
            return generateOutput(node)

        # execute on all adjacent nodes
        for (m, weight) in graph[node]:
            # put in the set of adjacent targets for next iteration
            if m not in visit_list and m not in done_list:
                addToVisitList(m, weight, node)

            # check if its better to visit and update
            else:
                changeNodePath(m, weight, node)

        # move node to visited ones because neighbours were visited
        visit_list.remove(node)
        done_list.add(node)

    print('Path does not exist!')
    return None


result = a_star_algorithm()
print('\n--------------------')

for node in result:
    print(node, end='  ')

print('\n--------------------\n')
