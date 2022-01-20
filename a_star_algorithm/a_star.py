adjacent_nodes = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('D', 5)],
    'C': [('D', 12)]
}

heuristic = {
    'A': 1,
    'B': 1,
    'C': 1,
    'D': 1
}

start = 'A'
stop = 'D'

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

    print('Path found: {}'.format(result))
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
        for (m, weight) in adjacent_nodes[node]:
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


a_star_algorithm()
