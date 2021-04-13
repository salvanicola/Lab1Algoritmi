# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import logging
import multiprocessing
from multiprocessing import Process

from dfs import dfs
from graph import graph_generator, Graph
import matplotlib.pyplot as plt
import time
import glob
import math

from kruskal_naive import kruskalNaive
from prim import prim

###################
# mac fix
import re

numbers = re.compile(r'(\d+)')

logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def numerical_sort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


####################

# ho dovuto ordinare i file per nome (ty stefano lavori)
def upload_graph():
    files = glob.glob("mst_dataset/*.txt")
    graphs = []
    for infile in sorted(glob.glob("mst_dataset/*.txt"), key=numerical_sort):
        graphs.append(graph_generator(infile))
    return graphs


def exec_threading(graph):
    # root = x.arch_list[0].vert1
    start_time = time.time()
    kruskalNaive(graph)
    stop_time = time.time() - start_time
    logger.debug("--- %s seconds ---" % stop_time)
    return stop_time, graph.n_vertexes * graph.n_arches


if __name__ == '__main__':

    graphs = upload_graph()
    index = 0
    times = []
    complexity = []

    p = multiprocessing.Pool(processes=graphs.__len__())
    data = p.map(exec_threading, [x for x in graphs])

    for x in data:
        times.append(x[0])
        complexity.append(x[1])

    plt.plot(complexity, times)
    temp = 0
    for x in range(0, len(times)):
        temp = temp + times[x] / complexity[x]
    temp = temp / len(times)
    plt.plot(complexity, [x * temp for x in complexity])
    plt.ylabel('Operation time')
    plt.xlabel('m * n')
    plt.show()
