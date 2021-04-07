# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Press the green button in the gutter to run the script.
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
    graphs = upload_graph()
    for x in graphs:
        root = x.list[0].vert1
        prim(x, root)
    print(" the end ")
