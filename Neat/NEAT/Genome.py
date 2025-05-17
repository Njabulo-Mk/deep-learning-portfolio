import random

from Connection import Connection
from InnovationNumber import InnovationNumber
from Node import Node, NodeType
from Bird import Bird


class Genome:
    def __init__(self):
        self.nodes = {}
        self.connections = {}
        self.init()
        self.fitness = 0
        self.bird = Bird(100, random.uniform(200, 500))
        self.alive = True
        self.in_pipe = False
        self.shared_fitness = 0

    '''Add node to the genome'''
    def add_node(self, node):
        self.nodes[node.node_id] = node

    '''add connection in the genome'''
    def add_connections(self, conn):
        self.connections[conn.innovation_number] = conn

    '''node mutation - select connection, add the node in-between'''
    def node_mutation(self):
        node = Node(len(self.nodes), NodeType.HIDDEN)
        enable_conns = [c for c in self.connections.values() if c.get_state()]

        if not enable_conns:
            return

        conn = random.choice(enable_conns)
        conn.toggle_enable()

        innov1 = InnovationNumber.get_innovation_number(conn.in_, node)
        conn1 = Connection(conn.in_, node, 1, innov1)
        node.add_in_connection(conn1)

        innov2 = InnovationNumber.get_innovation_number(node, conn.out)
        conn2 = Connection(node, conn.out, conn.weight, innov2)
        conn.out.add_in_connection(conn2)

        self.add_node(node)
        self.add_connections(conn1)
        self.add_connections(conn2)

    '''
    connection-mutation - select two node connect them if are not the same or not a input to output connection
    '''
    def connection_mutation(self):
        node1, node2 = random.sample(list(self.nodes.values()), 2)

        if not self.is_connected(node1, node2) and node1.node_id != node2.node_id and \
                node1.node_type != NodeType.INPUT and node2.node_type != NodeType.OUTPUT:
            num = random.uniform(-1, 1)
            innov = InnovationNumber.get_innovation_number(node1, node2)
            conn = Connection(node1, node2, num, innov)
            node2.add_in_connection(conn)
            self.add_connections(conn)

    '''check to see if the are connections in the nodes'''
    def is_connected(self, node1, node2):
        for conn in self.connections.values():
            if (conn.in_.node_id == node1.node_id and conn.out.node_id == node2.node_id) or \
                    (conn.in_.node_id == node2.node_id and conn.out.node_id == node1.node_id):
                return True
        return False

    '''mutate by calling the mutation and the different weights'''
    def mutate(self, add_node_rate=0.3, add_conn_rate=0.6, adjust_weight_rate=0.8, perturb=0.3):

        if random.random() < add_node_rate:
            self.node_mutation()
        if random.random() < add_conn_rate:
            self.connection_mutation()
        if random.random() < adjust_weight_rate:
            for conn in self.connections.values():
                conn.mutate_weight(perturb)

    '''get inputs and use the topological sort. calculate the activation and calculate the output. make decision.'''
    def flap_decision(self, inputs):
        self.nodes.get(0).set_input_value(inputs[0])
        self.nodes.get(1).set_input_value(inputs[1])
        self.nodes.get(2).set_input_value(inputs[2])
        self.nodes.get(3).set_input_value(inputs[3])
        self.nodes.get(4).set_input_value(inputs[4])

        sorted_nodes = self.topological_sort()

        for node in sorted_nodes:
            node.calculate_activation()

        output_node = self.nodes.get(5)
        output_activation = output_node.activate

        print(output_activation)
        if output_activation > 0.5:
            return 1
        else:
            return 0

    '''get the alive boolean and decision'''
    def update_bird(self, alive, inputs):
        self.bird.update(alive, self.flap_decision(inputs))

    '''make the initial network'''
    def init(self):
        bird_y = Node(0, NodeType.INPUT)
        bird_vel = Node(1, NodeType.INPUT)
        bird_pipe_dis = Node(2, NodeType.INPUT)
        pipe_center = Node(3, NodeType.INPUT)
        y_pipe_center = Node(4, NodeType.INPUT)
        output = Node(5, NodeType.OUTPUT)

        conn1 = Connection(bird_y, output, random.uniform(-0.5, 0.5),
                           InnovationNumber.get_innovation_number(bird_y, output))
        conn2 = Connection(bird_vel, output, random.uniform(-0.5, 0.5),
                           InnovationNumber.get_innovation_number(bird_vel, output))
        conn3 = Connection(bird_pipe_dis, output, random.uniform(-0.5, 0.5),
                           InnovationNumber.get_innovation_number(bird_pipe_dis, output))
        conn4 = Connection(pipe_center, output, random.uniform(-0.5, 0.5),
                           InnovationNumber.get_innovation_number(pipe_center, output))
        conn5 = Connection(y_pipe_center, output, random.uniform(-0.5, 0.5),
                           InnovationNumber.get_innovation_number(pipe_center, output))

        self.add_node(bird_y)
        self.add_node(bird_vel)
        self.add_node(bird_pipe_dis)
        self.add_node(pipe_center)
        self.add_node(y_pipe_center)
        self.add_node(output)

        self.add_connections(conn1)
        self.add_connections(conn2)
        self.add_connections(conn3)
        self.add_connections(conn4)
        self.add_connections(conn5)

        output.add_in_connection(conn1)
        output.add_in_connection(conn2)
        output.add_in_connection(conn3)
        output.add_in_connection(conn4)
        output.add_in_connection(conn5)

    '''sort the network'''
    def topological_sort(self):
        visited = set()
        sorted_nodes = []

        def visit(node):
            if node not in visited:
                visited.add(node)
                for conn in node.in_conns:
                    visit(conn.in_)
                sorted_nodes.append(node)

        for node in self.nodes.values():
            visit(node)

        return sorted_nodes
