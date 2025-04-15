import uuid

class CertificateAuthority:
    def __init__(self):
        self.certificates = {}  # Stores node certificates
    
    def generate_certificate(self, node_id):
        """
        Generates a unique certificate for the node using uuid.
        """
        certificate = str(uuid.uuid4())
        self.certificates[node_id] = certificate
        print(f"Certificate generated for {node_id}: {certificate}")
        return certificate

    def revoke_certificate(self, node_id):
        """
        Revokes the certificate of the given node.
        """
        if node_id in self.certificates:
            print(f"Certificate for {node_id} has been revoked.")
            del self.certificates[node_id]
        else:
            print(f"No certificate found for {node_id}.")

    def validate_certificate(self, node_id):
        """
        Checks if the node's certificate is still valid.
        """
        return node_id in self.certificates
