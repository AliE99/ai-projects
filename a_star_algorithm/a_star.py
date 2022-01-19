

adjac_lis = {
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


def a_star(start, stop):
    # nodes that have been visited but adjacent nodes haven't been visited yet
    visited_list = set([start])
    done_list = set([])

    # present distances from start to all other nodes
    distance = {}
    distance[start] = 0

    parent = {}
    parent[start] = start

    # select node with lowest f
    while len(visited_list) > 0:
        n = None
        for v in visited_list:
            if n == None or distance[v] + heuristic[v] < distance[n] + heuristic[n]:
                n = v

        if n == None:
            print(f"There is no path from {start} to {stop}")
            return None

        if n == stop:
            reconst_path = []

            while parent[n] != n:
                reconst_path.append(n)
                n = parent[n]

            reconst_path.append(start)

            reconst_path.reverse()

            print('Path found: {}'.format(reconst_path))
            return reconst_path

        # for all the neighbors of the current node do
        for (m, weight) in adjac_lis[n]:
            # if the current node is not presentin both open_lst and closed_lst
            # add it to open_lst and note n as it's par
            if m not in visited_list and m not in done_list:
                visited_list.add(m)
                parent[m] = n
                distance[m] = distance[n] + weight

            # otherwise, check if it's quicker to first visit n, then m
            # and if it is, update par data and poo data
            # and if the node was in the closed_lst, move it to open_lst
            else:
                if distance[m] > distance[n] + weight:
                    distance[m] = distance[n] + weight
                    parent[m] = n

                    if m in done_list:
                        done_list.remove(m)
                        visited_list.add(m)

        # remove n from the open_lst, and add it to closed_lst
        # because all of his neighbors were inspected
        visited_list.remove(n)
        done_list.add(n)

    print('Path does not exist!')
    return None


a_star('A', 'D')
