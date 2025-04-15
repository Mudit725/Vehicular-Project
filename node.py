from flask import Flask, request, jsonify
import requests
from certificates import CertificateAuthority

# Initialize the certificate authority
certificate_authority = CertificateAuthority()

class Node:
    def __init__(self, node_id, ip, port, blockchain):
        self.node_id = node_id
        self.blockchain = blockchain
        self.message_log = []
        self.ip = ip
        self.port = port
        self.neighbor_nodes = []
        self.certificate = certificate_authority.generate_certificate(node_id)  # Generate a certificate for the node
        self.is_valid = True
        self.revoked = False
        self.server = None

    def send_message(self, message, to_ip, to_port):
        if not self.is_valid or self.revoked:
            print(f"Node {self.node_id} is invalid or revoked and cannot send messages.")
            return

        # Validate the certificate before sending
        if not certificate_authority.validate_certificate(self.node_id):
            print(f"Certificate for {self.node_id} is no longer valid.")
            return

        data = {'node_id': self.node_id, 'message': message}
        self.blockchain.add_block(data)
        self.message_log.append(data)
        print(f"Node {self.node_id} sent a message: {message}")

        # Send the message to the destination node
        url = f'http://{to_ip}:{to_port}/receive_message'
        try:
            response = requests.post(url, json=data)
            if response.status_code == 200:
                print(f"Message delivered to Node at {to_ip}:{to_port}")
            else:
                print(f"Failed to deliver message to {to_ip}:{to_port}")
        except Exception as e:
            print(f"Error: {e}")


    def broadcast_message(self, message):
        """
        Broadcasts a message to all neighbor nodes.
        """
        if not self.is_valid or self.revoked:
            print(f"Node {self.node_id} is invalid or revoked and cannot broadcast messages.")
            return

        # Validate the certificate before broadcasting
        if not certificate_authority.validate_certificate(self.node_id):
            print(f"Certificate for {self.node_id} is no longer valid.")
            return

        data = {'node_id': self.node_id, 'message': message}
        self.blockchain.add_block(data)
        self.message_log.append(data)
        print(f"Node {self.node_id} broadcasted a message: {message}")

        # Send the message to all neighbors
        for neighbor in self.neighbor_nodes:  # Neighbor is a Node object, not (ip, port) tuple
            url = f'http://{neighbor.ip}:{neighbor.port}/receive_message'
            try:
                response = requests.post(url, json=data)
                if response.status_code == 200:
                    print(f"Message delivered to Node at {neighbor.ip}:{neighbor.port}")
                else:
                    print(f"Failed to deliver message to {neighbor.ip}:{neighbor.port}")
            except Exception as e:
                print(f"Error: {e}")


    def receive_message(self, message_data):
        sender_id = message_data['node_id']
        message = message_data['message']
        print(f"Node {self.node_id} received message from Node {sender_id}: {message}")
        self.log_activity(sender_id, message)

    def log_activity(self, sender_id, message):
        data = {'sender_id': sender_id, 'message': message}
        self.blockchain.add_block(data)

        if "fake" in message.lower() or "alert" in message.lower():
            print(f"Malicious activity detected from {sender_id}!")
            self.revoke_node(sender_id)

    def revoke_node(self, sender_id):
        if sender_id == self.node_id:
            self.revoked = True
            certificate_authority.revoke_certificate(sender_id)
            print(f"Node {sender_id} has been revoked and can no longer send messages.")

    def recover_node(self):
        self.revoked = False
        self.is_valid = True
        print(f"Node {self.node_id} has been recovered and can now send messages again.")

    def run_server(self):
        app = Flask(__name__)

        @app.route('/receive_message', methods=['POST'])
        def receive_message():
            message_data = request.get_json()
            self.receive_message(message_data)
            return jsonify({"status": "Message received successfully"}), 200

        self.server = app
        app.run(host=self.ip, port=self.port)

    def add_neighbor(self, ip, port):
        self.neighbor_nodes.append((ip, port))
