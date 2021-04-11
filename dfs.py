from collections import deque

from matplotlib.cbook import Stack


def dfs(graph):
    for v in graph.vert_list:
        if v.flag is False:
            if dfs_traversal(graph, v) is True:
                return True
    return False


def dfs_traversal(graph, s):

    # Create a stack for DFS
    stack = deque()

    # Push the current source node.
    stack.append(s)

    while len(stack) > 0:
        # Pop a vertex from stack
        v = stack.pop()

        # Stack may contain same vertex twice. So
        # we need to print the popped item only
        # if it is not visited.
        if not visited[s]:
            print(s, end=' ')
            visited[s] = True

        # Get all adjacent vertices of the popped vertex s
        # If a adjacent has not been visited, then push it
        # to the stack.
        for node in graph.arch_list:

            if not visited[node]:
                stack.append(node)
