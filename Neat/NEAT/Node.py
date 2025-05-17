import math
from enum import Enum

'''
Type of nodes.
'''


class NodeType(Enum):
    INPUT = 0,
    OUTPUT = 1,
    HIDDEN = 2


def activation_function(x):
    x = max(-500, min(500, x))
    return 1 / (1 + math.exp(-x))


class Node:
    def __init__(self, node_id, node_type):
        # set node type
        # set id
        # activate value
        # connections that come in the nodes
        self.node_type = node_type
        self.node_id = node_id
        self.activate = 0.0
        self.in_conns = []

    '''
    add connections that are are not already in the list
    '''
    def add_in_connection(self, conn):
        if conn not in self.in_conns:
            self.in_conns.append(conn)

    '''
    calculate the weight sum and then put in they activation function.
    '''
    def calculate_activation(self):
        if self.node_type != NodeType.INPUT:
            total_input = sum(conn.weight * conn.in_.activate for conn in self.in_conns if conn.enable)
            self.activate = activation_function(total_input)
        return self.activate

    '''
    set input values.
    '''
    def set_input_value(self, value):
        if self.node_type == NodeType.INPUT:
            self.activate = value
