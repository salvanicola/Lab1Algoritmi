from collections import deque

import logging


def dfs(graph):
    for v in graph.vert_list:
        if v is not None:
            if v.flag is False:
                if dfs_iter(graph, v) is True:
                    return True
    return False


def dfs_rec(graph, vert):
    vert.flag = True
    for arch in graph.arch_list:
        if arch.label is None:
            opposite = None
            if arch.vert1 == vert.id:
                opposite = graph.vert_list[arch.vert2]
            elif arch.vert2 == vert.id:
                opposite = graph.vert_list[arch.vert1]
            if opposite is not None:
                if opposite.flag is False:
                    arch.label = "discovery"
                    if dfs_rec(graph, opposite) is True:
                        return True
                else:
                    arch.label = "back"
                    return True
    return False


def dfs_iter(graph, s):
    stack = deque()
    stack.append(s)
    while len(stack):
        s = stack.pop()
        s.flag = True
        for x in graph.incident_edges(s):
            if x.label is None:
                v = graph.vert_list[x.opposite(s.id)]
                if v.flag is False:
                    x.label = "DISCOVERY"
                    v.flag = True
                    stack.append(v)
                else:
                    x.label = "BACK"
                    return True
    return False
