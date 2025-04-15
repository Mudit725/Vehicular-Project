def generate_report(nodes, blockchain, malicious_node=None):
    with open('ledger_report.txt', 'w') as report:
        report.write("Blockchain Ledger Report\n")
        report.write("========================\n\n")
        
        # Node to certificate mapping before the removal
        report.write("Node to Certificate Mappings (Before Removal)\n")
        report.write("=============================================\n")
        for node in nodes:
            report.write(f"{node.node_id}: {node.certificate}\n")
        report.write("\n")

        # Ledger report
        for block in blockchain.chain:
            report.write(f"Block Index: {block.index}\n")
            report.write(f"Timestamp: {block.timestamp}\n")
            report.write(f"Data: {block.data}\n")
            report.write(f"Previous Hash: {block.previous_hash}\n")
            report.write(f"Hash: {block.hash}\n")
            report.write("-" * 30 + "\n")

        report.write("\nMalicious Node Tracking\n")
        report.write("=======================\n")
        if malicious_node:
            report.write(f"The fake alert was sent by {malicious_node.node_id}, and its certificate has been revoked.\n")

        # Node to certificate mapping after the removal
        remaining_nodes = [node for node in nodes if node.node_id != malicious_node.node_id]
        report.write("\nNode to Certificate Mappings (After Removal)\n")
        report.write("============================================\n")
        for node in remaining_nodes:
            report.write(f"{node.node_id}: {node.certificate}\n")
