# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
import logging

from graph import graph_generator, Graph
import glob


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

    for x in graphs:
        root = x.list[0].vert1
        # thread = threading.Thread(target=prim, args=(x, root))
        # threads.append(thread)
        # logger.debug("create and start thread number %s", index)
        # thread.start()
        prim(x, root)
        index = index + 1

    # for index, thread in enumerate(threads):
    #     thread.join()
    logger.debug(" the end ")
