import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
import threading

def receive_messages(client_socket, cipher):
    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
            decrypted_message = cipher.decrypt(encrypted_message)
            print(f"Message: {decrypted_message.decode()}")
        except:
            print("Connection closed.")
            break

def start_client(server_ip):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, 9999))
    print("Connected to the server.")

    # Receive the server's public key
    public_pem = client.recv(1024)
    
    # Load the public key
    public_key = serialization.load_pem_public_key(public_pem)

    # Generate a symmetric key (Fernet)
    symmetric_key = Fernet.generate_key()
    cipher = Fernet(symmetric_key)

    # Encrypt the symmetric key with the server's public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Send the encrypted symmetric key to the server
    client.send(encrypted_symmetric_key)

    # Start receiving messages
    thread = threading.Thread(target=receive_messages, args=(client, cipher))
    thread.start()

    try:
        while True:
            message = input("You: ")
            if message.lower() == 'exit':
                break
            encrypted_message = cipher.encrypt(message.encode())
            client.send(encrypted_message)
    finally:
        client.close()

if __name__ == "__main__":
    start_client('127.0.0.1')  # Replace with the server's IP
