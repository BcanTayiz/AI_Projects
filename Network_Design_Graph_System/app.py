import streamlit as st
from network.graph import create_graph, add_node, add_edge
from network.metrics import calculate_metrics
from components.graph_viewer import display_graph
from network.ai_optimizer import suggest_improvements

# Initialize session state for network graph
if 'G' not in st.session_state:
    st.session_state.G = create_graph()

G = st.session_state.G

st.title("Network Design & Optimization System")

# Streamlit "slides"
slide = st.radio("Select Slide", ["Design Network", "Set Parameters", "View KPIs", "AI Suggestions"])

# -----------------------------
# Slide 1: Design Network
# -----------------------------
if slide == "Design Network":
    st.subheader("Add Nodes")
    node_name = st.text_input("Node name")
    node_type = st.selectbox("Node type", ["Router", "Switch", "Server"])
    if st.button("Add Node") and node_name:
        add_node(G, node_name, node_type)
        st.success(f"Added node: {node_name}")

    st.subheader("Add Edges")
    if len(G.nodes) >= 2:
        node1 = st.selectbox("Node 1", G.nodes)
        node2 = st.selectbox("Node 2", G.nodes)
        if node1 != node2:
            if st.button("Add Edge"):
                add_edge(G, node1, node2)
                st.success(f"Added edge: {node1}-{node2}")

# -----------------------------
# Slide 2: Set Parameters
# -----------------------------
elif slide == "Set Parameters":
    st.subheader("Update Edge Parameters")
    if G.number_of_edges() == 0:
        st.info("Add edges first in the Design Network slide.")
    else:
        for u, v, data in G.edges(data=True):
            st.write(f"Edge {u} - {v}")
            bandwidth = st.number_input(f"Bandwidth {u}-{v}", value=data.get('bandwidth', 100))
            latency = st.number_input(f"Latency {u}-{v}", value=data.get('latency', 10))
            data['bandwidth'] = bandwidth
            data['latency'] = latency

# -----------------------------
# Slide 3: View KPIs
# -----------------------------
elif slide == "View KPIs":
    st.subheader("Network KPIs")
    if G.number_of_edges() == 0:
        st.info("Add edges first to calculate KPIs.")
    else:
        total_bandwidth, avg_latency, total_cost = calculate_metrics(G)
        st.metric("Total Bandwidth", total_bandwidth)
        st.metric("Average Latency", avg_latency)
        st.metric("Total Cost", total_cost)
        st.subheader("Network Graph")
        display_graph(G)

# -----------------------------
# Slide 4: AI Suggestions
# -----------------------------
elif slide == "AI Suggestions":
    st.subheader("AI Optimization Suggestions")
    if G.number_of_edges() == 0:
        st.info("Add edges first to get AI suggestions.")
    else:
        suggestions = suggest_improvements(G)
        for s in suggestions:
            st.info(s)
