def suggest_improvements(G):
    suggestions = []

    # Find edge with lowest bandwidth (bottleneck)
    if G.number_of_edges() > 0:
        min_bandwidth_edge = min(G.edges(data=True), key=lambda x: x[2].get('bandwidth', 0))
        suggestions.append(f"Increase bandwidth on edge {min_bandwidth_edge[0]}-{min_bandwidth_edge[1]}")

    # Find edge with highest latency
    max_latency_edge = max(G.edges(data=True), key=lambda x: x[2].get('latency', 0), default=None)
    if max_latency_edge:
        suggestions.append(f"Reduce latency on edge {max_latency_edge[0]}-{max_latency_edge[1]}")

    # Suggest new connection between nodes with high degree difference
    node_degrees = dict(G.degree())
    if len(node_degrees) > 1:
        high_degree = max(node_degrees, key=node_degrees.get)
        low_degree = min(node_degrees, key=node_degrees.get)
        if not G.has_edge(high_degree, low_degree):
            suggestions.append(f"Consider adding edge between {high_degree} and {low_degree} for better connectivity")

    if not suggestions:
        suggestions.append("Network is optimized based on current simple rules!")

    return suggestions
