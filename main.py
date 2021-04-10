# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import logging

from graph import graph_generator, Graph
import matplotlib.pyplot as plt
import numpy as np
import time
import glob
import math
import threading

from prim import prim


def upload_graph():
    files = glob.glob("mst_dataset/*.txt")
    graphs = []
    for x in files:
        graphs.append(graph_generator(x))
    return graphs


if __name__ == '__main__':

    logger = logging.getLogger('tipper')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    graphs = upload_graph()
    # threads = list()
    index = 0

    times = []
    complex = []
    for x in graphs:
        root = x.list[0].vert1
        # thread = threading.Thread(target=prim, args=(x, root))
        # threads.append(thread)
        # logger.debug("create and start thread number %s", index)
        # thread.start()
        start_time = time.time()
        prim(x, root)
        stop_time = time.time() - start_time
        logger.debug("--- %s seconds ---" % stop_time)
        index = index + 1
        times.append(stop_time)
        complex.append(x.n_vertexes + x.n_arches * math.log(x.n_arches))

    # for index, thread in enumerate(threads):
    #     thread.join()
    logger.debug(" the end ")
    plt.plot(complex, times)
    temp = 0
    for x in range(0, len(times)):
        temp = temp + times[x] / complex[x]
    temp = temp / len(times)
    plt.plot(complex, [x*temp for x in complex])
    plt.ylabel('Operation time')
    plt.xlabel('m + n * log(n)')
    plt.show()
