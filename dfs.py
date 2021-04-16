from collections import deque

import logging


def dfs(graph, n_vertex):
    visited_v = [False for i in range(n_vertex)]
    for v in graph.vert_list:
        if v is not None:
            if visited_v[v.id] is False:
                if dfs_iter(graph, v.id, visited_v) is True:
                    return True
    return False


# def dfs_rec(graph, vert, checker, out=False):
#     vert.flag = not checker
#     for arch in graph.arch_list:
#         if arch.label is checker:
#             opposite = None
#             if arch.vert1 == vert.id:
#                 opposite = graph.vert_list[arch.vert2]
#             elif arch.vert2 == vert.id:
#                 opposite = graph.vert_list[arch.vert1]
#             if opposite is not None:
#                 if opposite.flag is checker:
#                     arch.label = not checker
#                     if dfs_rec(graph, opposite, checker) is True:
#                         out = True
#                 else:
#                     out = True
#     return out


def dfs_iter(graph, s, visited_v):
    stack = deque()
    stack.append(s)
    while len(stack):
        s = stack[-1]
        stack.pop()

        if not visited_v[s]:
            visited_v[s] = True
        else:
            return True

        if graph.adj[s] is not None:
            for node in graph.adj[s]:
                if not visited_v[node]:
                    stack.append(node)
    return False

    # while len(stack):
    #     s = stack.pop()
    #     visited_v[s] = True
    #     for x in graph.arch_list:
    #         if x.label is None:
    #             opposite = None
    #             if x.vert1 == s.id:
    #                 opposite = graph.vert_list[x.vert2]
    #             elif x.vert2 == s.id:
    #                 opposite = graph.vert_list[x.vert1]
    #             if opposite is not None:
    #                 if opposite.flag is False:
    #                     x.label = "discovery"
    #                     opposite.flag = True
    #                     stack.append(opposite)
    #                 else:
    #                     return True

