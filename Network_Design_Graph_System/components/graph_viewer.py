from pyvis.network import Network
import streamlit.components.v1 as components

def display_graph(G, height=500):
    net = Network(height=f"{height}px", width="100%", notebook=False)
    net.from_nx(G)
    html_file = "temp_graph.html"
    net.save_graph(html_file)
    with open(html_file, 'r', encoding='utf-8') as f:
        components.html(f.read(), height=height)
