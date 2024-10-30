import socket
import threading
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.fernet import Fernet

# Generate RSA Key Pair (server)
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)

# Extract public key to send to the client
public_key = private_key.public_key()

# Serialize the public key to send to the client
# PEM format is a standard encoding format for public keys.
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Server to receive encrypted symmetric key and relay messages
def handle_client(client_socket, addr, clients):
    try:
        # Send the public key to the client
        client_socket.send(public_pem)
        
        # Receive the encrypted symmetric key
        encrypted_symmetric_key = client_socket.recv(1024)
        
        # Decrypt the symmetric key with the server's private key
        symmetric_key = private_key.decrypt(
            encrypted_symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Symmetric key received: {symmetric_key}")
        
        # Now use the symmetric key to encrypt/decrypt messages
        cipher = Fernet(symmetric_key)
        
        while True:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = cipher.decrypt(encrypted_message)
            print(f"Received from {addr}: {decrypted_message.decode()}")
            
            # Broadcast to other clients
            for client in clients:
                if client != client_socket:
                    client.send(encrypted_message)
    finally:
        # Cleanup on client disconnect
        client_socket.close()
        clients.remove(client_socket)
        print(f"Connection closed with {addr}")

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))
    server.listen(5)
    clients = []

    print("Server started, waiting for connections...")
    try:
        while True:
            client_socket, addr = server.accept()
            clients.append(client_socket)
            print(f"Connection from {addr}")
            thread = threading.Thread(target=handle_client, args=(client_socket, addr, clients))
            thread.start()
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
