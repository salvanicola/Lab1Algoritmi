# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import gc
import logging

from numpy import average

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


def plotting_plot(times, complexity):
    plt.plot(complexity, times)
    temp = 0
    for x in range(0, len(times)):
        temp = temp + times[x] / complex[x]
    temp = temp / len(times)
    plt.plot(complexity, [x * temp for x in complexity])
    plt.ylabel('Operation time')
    plt.xlabel('m')
    plt.show()


def testing(graphs, function, **args):
    times = []
    complexity = []
    current_instance = 0
    instance_list = []
    for x in graphs:
        if x.n_vertexes != current_instance:
            avg = average(instance_list)
            logger.debug("--- %s seconds --- for %s", avg, current_instance)
            times.append(average(instance_list))
            complexity.append(current_instance)
            instance_list = []
        gc.disable()
        start_time = time.perf_counter_ns()
        function(x)
        stop_time = time.perf_counter_ns()
        gc.enable()
        instance_list.append(stop_time - start_time)
        current_instance = x.n_vertexes
    avg = average(instance_list)
    logger.debug("--- %s seconds --- for %s", avg, current_instance)
    times.append(average(instance_list))
    complexity.append(current_instance)
    return times, complexity


if __name__ == '__main__':
    logger = logging.getLogger('tipper')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    graphs = upload_graph()
    times, complexity = testing(graphs, kruskalNaive)
    plotting_plot(times, complexity)
