import threading
from random import choice
from blockchain import Blockchain
from node import Node
from certificates import CertificateAuthority
from graph import plot_network  # Import graph plotting
from ledger_report import generate_report  # Import ledger reporting
import time

# Initialize Blockchain and Certificate Authority
blockchain = Blockchain()
certificate_authority = CertificateAuthority()

# Define IP and ports for each node (local IP, different ports)
node_configs = [
    {"node_id": "Node_1", "ip": "127.0.0.1", "port": 5000},
    {"node_id": "Node_2", "ip": "127.0.0.1", "port": 5001},
    {"node_id": "Node_3", "ip": "127.0.0.1", "port": 5002},
    {"node_id": "Node_4", "ip": "127.0.0.1", "port": 5003},
    {"node_id": "Node_5", "ip": "127.0.0.1", "port": 5004},
]

# Create a list of node objects
nodes = []
for config in node_configs:
    node = Node(config["node_id"], config["ip"], config["port"], blockchain)
    nodes.append(node)

# Set initial neighbors (randomly)
for node in nodes:
    possible_neighbors = [n for n in nodes if n.node_id != node.node_id]
    neighbors = choice(possible_neighbors)  # Assign one random neighbor
    node.neighbor_nodes = [neighbors]  # Make sure it's a list
    print(f"Neighbors for {node.node_id}: {[n.node_id for n in node.neighbor_nodes]}")


# Start servers in different threads
def start_node(node):
    node.run_server()


for node in nodes:
    thread = threading.Thread(target=start_node, args=(node,))
    thread.start()

# Add delay to ensure servers are running before starting communication
time.sleep(5)  # Delay for 5 seconds to allow all servers to start

# Step 1: Visualize the initial network before any message exchange
edges_before = [(node.node_id, neighbor.node_id) for node in nodes for neighbor in node.neighbor_nodes]
plot_network(nodes, edges_before, "Initial Network (Before Message Exchange)", "network_map_before.png")


# Function to simulate a single message exchange
def single_message_exchange():
    # Truthful message broadcast by Node_1
    nodes[0].broadcast_message("Traffic is smooth on Route A.")  # Truthful message
    time.sleep(2)  # Short wait for processing

    # Malicious message broadcast by Node_2
    nodes[1].broadcast_message("FAKE ALERT: Major accident on Route A!")  # False message


# Start the single message exchange simulation
single_message_exchange()

# Wait for a moment to ensure all messages are processed
time.sleep(2)

# Step 3: Blockchain validation and detection of malicious activity
blockchain.validate_chain()
malicious_node_id = blockchain.scan_for_malicious_activity()

# Track and revoke the malicious node if found
for node in nodes:
    if node.node_id == malicious_node_id:
        print(f"Malicious activity detected from {node.node_id}. Invalidating the node...")
        node.revoke_node(node.node_id)
        break

# Generate report of the blockchain ledger and tracking process
generate_report(nodes, blockchain, node if 'node' in locals() else None)  # Call the report function

# Step 6: Visualize the network after the message exchanges
remaining_nodes = [node for node in nodes if node.node_id != malicious_node_id]
edges_after = [(node.node_id, neighbor.node_id) for node in remaining_nodes for neighbor in node.neighbor_nodes]
plot_network(remaining_nodes, edges_after, "Network After Message Exchange", "network_map_after.png")
