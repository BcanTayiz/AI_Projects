def calculate_metrics(G):
    if G.number_of_edges() == 0:
        return 0, 0, 0
    total_bandwidth = sum([data.get('bandwidth', 0) for u,v,data in G.edges(data=True)])
    avg_latency = sum([data.get('latency', 0) for u,v,data in G.edges(data=True)]) / G.number_of_edges()
    total_cost = G.number_of_nodes()*100 + G.number_of_edges()*50
    return total_bandwidth, avg_latency, total_cost
