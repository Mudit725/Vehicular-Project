import matplotlib.pyplot as plt
import networkx as nx

def plot_network(nodes, edges, title, filename):
    G = nx.Graph()

    # Add nodes to the graph
    for node in nodes:
        G.add_node(node.node_id)

    # Add edges based on neighbor connections
    G.add_edges_from(edges)

    # Plot the network graph
    pos = nx.spring_layout(G)  # Create a layout for the graph
    nx.draw(G, pos, with_labels=False, node_color="lightblue", node_size=2000, font_size=10, font_weight='bold', edge_color="gray")
    
    # Add labels with spacing
    labels = {node.node_id: f"{node.node_id}\nCert: {node.certificate[:8]}" for node in nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=8)

    # Adjust label positions to add space
    for label, _ in labels.items():
        x, y = pos[label]  # Get the position of the label
        plt.text(x, y + 0.1, labels[label], fontsize=8, ha='center')  # Add a small vertical offset

    # Set title and save the plot as an image
    plt.title(title)
    plt.axis('off')  # Turn off the axis
    plt.tight_layout()  # Adjust layout to make room for the title and labels
    plt.savefig(filename, format='png')
    plt.show()
