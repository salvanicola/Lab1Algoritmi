# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import gc
import logging
from numpy import average
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


def plotting_plot(t, comp):
    references = [0.25 * size * size for size in comp]
    plt.plot(comp, t)
    plt.plot(comp, references)
    plt.ylabel('Operation time')
    plt.xlabel('n')
    plt.show()
    logger.debug("plotted")


def testing(g, function, **args):
    times = []
    complexity = []
    current_instance = 0
    instance_list = []
    for x in g:
        num_calls = 1
        if x.n_vertexes < 400:
            num_calls = 100
        if x.n_vertexes != current_instance:
            avg = average(instance_list)
            logger.debug("--- %s ns --- for %s", avg, current_instance)
            times.append(average(instance_list))
            complexity.append(current_instance)
            instance_list = []
        gc.disable()
        start_time = time.time()
        for i in range(num_calls):
            function(x)
        stop_time = time.time()
        gc.enable()
        instance_list.append((stop_time - start_time)/num_calls)
        current_instance = x.n_vertexes

    avg = average(instance_list)
    logger.debug("--- %s ns --- for %s", avg, current_instance)
    times.append(average(instance_list))
    complexity.append(current_instance)
    return times, complexity


logger = logging.getLogger('tipper')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

if __name__ == '__main__':
    graphs = upload_graph()
    times, complexity = testing(graphs, kruskalNaive)
    plotting_plot(times, complexity)
