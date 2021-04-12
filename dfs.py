def dfs(graph):
    for v in graph.vert_list:
        if v.flag is False:
            if dfs_rec(graph, v) is True:
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
