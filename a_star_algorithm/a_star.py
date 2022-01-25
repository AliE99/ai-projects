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

# nodes that have been visited but adjacent nodes haven't been visited yet
visit_list = set([start])
done_list = set([])

# present distances from start to all other nodes
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
    # select node with lowest f
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

        # for all the adjacent nodes of the current node do
        for (m, weight) in graph[node]:
            # add to visit list to be visited in the next iterate
            if m not in visit_list and m not in done_list:
                addToVisitList(m, weight, node)

            # otherwise, check if it's quicker to first visit node, then m
            # and if it is, update par data and poo data
            # and if the node was in the closed_lst, move it to open_lst

            else:
                changeNodePath(m, weight, node)

        # remove node from the open_lst, and add it to closed_lst
        # because all of his neighbors were inspected
        visit_list.remove(node)
        done_list.add(node)

    print('Path does not exist!')
    return None


result = a_star_algorithm()
print('\n--------------------')

for node in result:
    print(node, end='  ')

print('\n--------------------\n')
