import itertools
import sys
from graphviz import Source

"""
Takes in input from stdin
outputs huffman tree in graphviz's dot language to stdout
"""

# stdin and stdout is utf8
# other encoding will not work
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)
sys.stdin = open(sys.stdin.fileno(), mode='r', encoding='utf8', buffering=1)
sys.stderr = open(sys.stderr.fileno(), mode='w', encoding='utf8', buffering=1)


class NodeTree(object):
    """Holds information about each node"""
    id_iter = itertools.count()  # unique ID for each object

    def __init__(self, left: object = None, right: object = None, value: int = None, symbol: chr = None):
        """left and right point to a NodeTree object symbol is the character"""
        self.left = left
        self.right = right
        self.value = value
        self.symbol = symbol
        self.id = next(NodeTree.id_iter)  # unique ID for each object


freq: dict[chr, int] = {}  # declare dictionary to hold frequency of characters

# calculate frequency of characters
while True:
    char: chr = sys.stdin.read(1)
    while not char.isprintable():
        char = sys.stdin.read(1)
    if not char:
        break
    if char in freq:
        freq[char] += 1
    else:
        freq[char] = 1

# dictionary to list of tuples of (characters, frequency) and sort list
freq_list: list[tuple[chr, int]] = sorted(freq.items(), key=lambda x: x[1], reverse=True)

# a list of NodeTree objects
nodes: list[NodeTree] = []

# for each item in the frequency list convert to NodeTree object and append it to the list of nodes
for item in freq_list:
    nodes.append(NodeTree(None, None, item[1], item[0]))

# sort the list of nodes by value decreasing
nodes.sort(key=lambda x: x.value, reverse=True)

while len(nodes) > 1:
    # generate a new NodeTree object using last two items from nodes list
    # value of new node will be the sum of the values of the last two items in the nodes list
    new_node: NodeTree = NodeTree(nodes[-1], nodes[-2], nodes[-1].value + nodes[-2].value, None)
    # remove last two items from nodes list and append new node to the nodes list
    nodes = nodes[:-2]
    nodes.append(new_node)
    # sort the list of nodes by value decreasing
    nodes.sort(key=lambda x: x.value, reverse=True)


def tree_gen(tree: NodeTree) -> str:
    """DFS through tree and generate grahviz dot language"""

    node_str: str = ""
    edges: str = ""

    stack: list[NodeTree] = [tree]
    while stack:
        node = stack.pop()
        # generate nodes
        # check if the node is a symbol node or a value node
        if not node.symbol:
            node_str += "node [shape=circle fixedsize=true]\n\t" + '"N_' + str(node.id) + '" ' + '[ label = "' + str(
                node.value) + '" ]' + ';' + '\n\t'
        else:
            # add escape characters
            if (node.symbol == '\\' or node.symbol == "\"" or node.symbol == ">" or node.symbol == "<"
                    or node.symbol == "{" or node.symbol == "}" or node.symbol == "|"):
                temp_sym = "\\" + node.symbol
            else:
                temp_sym = node.symbol
            node_str += "node [shape=record fixedsize=true]\n\t" + '"N_' + str(node.id) + '" ' + '[ label = "{' + str(
                node.value) + " | " + temp_sym + '}" ]' + ';' + '\n\t'
        # generate edges
        if node.right:
            stack.append(node.right)
            edges += '"N_' + str(node.id) + '" ->  ' + '"N_' + str(node.right.id) + '";' + '\n\t'

        if node.left:
            stack.append(node.left)
            edges += '"N_' + str(node.id) + '" ->  ' + '"N_' + str(node.left.id) + '";' + '\n\t'
    # put everything together
    out: str = "digraph huffman { \n\t" + node_str + "\n\t" + edges + "}"
    return out


s: str = tree_gen(nodes[0])

# view and save graph
graph: Source = Source(s, filename="huffman_encoding_tree", format="svg")
graph.view()

# output tree to stdin
print(s)
