from collections import deque

import logging


def dfs(graph):
    for v in graph.vert_list:
        if v.flag is False:
            if dfs_iter(graph, v) is True:
                return True
    return False


def dfs_rec(graph, vert):
    if not vert.flag:
        vert.flag = True
        for arch in graph.arch_list:
            if arch.vert1 == vert:
                return dfs_rec(graph, arch.vert2)
            elif arch.vert2 == vert:
                return dfs_rec(graph, arch.vert1)
            else:
                return False
    else:
        return True


def dfs_iter(graph, s):
    stack = deque()
    stack.append(s)
    while len(stack):
        s = stack.pop()
        if s.flag is False:
            s.flag = True
        for x in graph.incident_edges(s):
            if x.label is None:
                v = graph.vert_list[x.opposite(s.id)]
                if v.flag is False:
                    x.label = "DISCOVERY"
                    stack.append(v)
                else:
                    x.label = "BACK"
                    return True
    return False
