import networkx as nx

def create_graph():
    G = nx.Graph()
    return G

def add_node(G, node_name, node_type="Router"):
    G.add_node(node_name, type=node_type)

def add_edge(G, node1, node2, bandwidth=100, latency=10):
    G.add_edge(node1, node2, bandwidth=bandwidth, latency=latency)
