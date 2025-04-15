import hashlib
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, data, hash):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.data = data
        self.hash = hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = self.create_block("Genesis Block", "0")
        self.chain.append(genesis_block)

    def create_block(self, data, previous_hash):
        index = len(self.chain)
        timestamp = time.time()
        hash = self.hash_block(index, previous_hash, timestamp, data)
        return Block(index, previous_hash, timestamp, data, hash)

    def hash_block(self, index, previous_hash, timestamp, data):
        block_string = "{}{}{}{}".format(index, previous_hash, timestamp, data)
        # Generate a full SHA256 hash, but return only the first 8 characters for readability
        return hashlib.sha256(block_string.encode()).hexdigest()[:8]

    def add_block(self, data):
        previous_block = self.chain[-1]
        new_block = self.create_block(data, previous_block.hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Data: {block.data}")
            print(f"Hash: {block.hash}")
            print("-" * 30)

    def validate_chain(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.previous_hash != previous_block.hash:
                print(f"Blockchain tampered at block {i}")
                return False

            recalculated_hash = self.hash_block(current_block.index, current_block.previous_hash, current_block.timestamp, current_block.data)
            if recalculated_hash != current_block.hash:
                print(f"Invalid hash at block {i}")
                return False

        print("Blockchain is valid.")
        return True
    def scan_for_malicious_activity(self):
        """
        Scan the blockchain for any records of malicious activities (e.g., fake alerts).
        """
        for block in self.chain:
            data = block.data
            if isinstance(data, dict) and "message" in data:
                message = data["message"]
                if "fake" in message.lower() or "alert" in message.lower():
                    print(f"Malicious activity found in block {block.index}: {message}")
                    # Return the node ID that sent the fake message
                    return data['node_id']
