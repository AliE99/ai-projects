# Prim's Algorithm applied to City Grid

INF = 999999
N = 7
#Adjacency Matrix for The City
City = [[0, 8, 0, 3, 0, 2, 4],
        [8, 0, 3, 2, 0, 0, 0],
        [0, 3, 0, 1, 2, 0, 0],
        [3, 2, 1, 0, 3, 5, 0],
        [0, 0, 2, 3, 0, 7, 0],
        [2, 0, 0, 5, 7, 0, 5],
        [4, 0, 0, 0, 0, 5, 0]]

House = [0, 0, 0, 0, 0, 0, 0]

Streets = 0

House[0] = True

print(" Streets : \n")
while (Streets < N - 1):

    minimum = INF
    a = 0
    b = 0
    for m in range(N):
        if House[m]:
            for n in range(N):
                if ((not House[n]) and City[m][n]):
                    if minimum > City[m][n]:
                        minimum = City[m][n]
                        a = m
                        b = n
    print(str(a) + "->" + str(b) + " with cost : " + str(City[a][b]))
    House[b] = True
    Streets += 1
