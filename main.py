#!/bin/python3

import heapq


class Node:
    def __init__(self, x, y, label, dist):
        self.distance = dist
        self.x = x
        self.y = y
        self.label = label
        self.parent = None
        self.connections = list()

    def add_connection(self, n):
        self.connections.append(n)

    def __lt__(self, other):
        return self.distance < other.distance


def make_graph(grid):
    """
    Makes a graph from the provided grid
    :param grid: list of lists with valid and invalid positions
    :return: list of Node objects and end position
    """
    graph = [None]*len(grid)*len(grid)
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] in ['.','e']:
                graph[i*len(grid) + j] = Node(i, j, i*len(grid) + j, 1000)
                if grid[i][j] == 'e':
                    endpos = (i, j)
            elif grid[i][j] == 's':
                graph[i * len(grid) + j] = Node(i, j, i * len(grid) + j, 0)

    N = len(grid)
    for i in range(len(grid)):
        for j in range(len(grid)):
            n = graph[i * len(grid) + j]
            if n is not None:
                if i < N - 1 and graph[(i + 1) * len(grid) + j] is not None:
                    graph[(i + 1) * len(grid) + j].add_connection(n)
                if i > 0 and graph[(i - 1) * len(grid) + j] is not None:
                    graph[(i - 1) * len(grid) + j].add_connection(n)
                if j < N - 1 and graph[i * len(grid) + j + 1] is not None:
                    graph[i * len(grid) + j + 1].add_connection(n)
                if j > 0 and graph[i * len(grid) + j - 1] is not None:
                    graph[i * len(grid) + j - 1].add_connection(n)
    return [i for i in graph if i is not None], endpos


def minimum_moves(grid):
    """
    Dijkstra algorithm
    :param grid: original grid, transformed then to a graph with make_graph
    :return: path from start to goal. List of tuples (x,y)
    """
    graph, endPos = make_graph(grid)

    while len(graph) > 0:
        heapq.heapify(graph)
        n = heapq.heappop(graph)
        if n.distance == 1000:
            return None
        if n.x == endPos[0] and n.y == endPos[1]:
            break
        for i in n.connections:
            if i.label in [j.label for j in graph]:
                if i.distance > n.distance + 1:
                    i.distance = n.distance + 1
                    i.parent = n

    solution = list()
    while n.parent is not None:
        solution.append((n.x, n.y))
        n = n.parent
    solution.append((n.x, n.y))

    return solution[::-1]

if __name__ == "__main__":

    grid = ['eX.X.',
            '.X...',
            '.sXXX',
            '..XX.',
            '.....']

    # Transform from list of strings to list of lists
    for ind, i in enumerate(grid):
        grid[ind] = [j for j in i]

    # Print grid
    for i in grid:
        print(i)
    print()
    solution = minimum_moves(grid)

    if solution is None:
        print('No solution for this start-end combination')
        quit()
    # mark the path
    for i in solution[1:-1]:
        grid[i[0]][i[1]] = 'o'
    # print grid with solution
    for i in grid:
        print(i)


