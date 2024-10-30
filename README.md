# Alma - Encrypted Messaging App

Alma is a secure messaging application designed to facilitate encrypted communication between users. Utilizing a combination of asymmetric and symmetric encryption, Alma ensures that messages remain private and secure during transmission. This repository contains both the server and client implementations of the application.

## Features

- **End-to-End Encryption**: Messages are encrypted before they are sent, ensuring only intended recipients can read them.
- **Asymmetric and Symmetric Encryption**: Utilizes RSA for key exchange and Fernet for message encryption.
- **Multi-client Support**: The server can handle multiple client connections simultaneously.

## Getting Started

### Prerequisites

- Python 3.x
- Required libraries:
  - `cryptography`

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/alma.git
   cd alma

2. Install the required libraries:

   ```bash
   pip install cryptography

## Running the application

1. Start the Server: Run the server script:

   ```bash
   python server.py

2. Start the Client: Open another terminal and run the client script:

   ```bash
   python server.py

  Replace '127.0.0.1' in client.py with the server's IP address if not running on the same machine.

## Network Considerations

When running the server and clients on different machines, you may need to consider the following:

- Port Forwarding: If the server is behind a router, you may need to configure port forwarding to allow external clients to connect to the server. Forward port 9999 (or your chosen port) to the internal IP address of the machine running the server.
- Firewall Settings: Ensure that the firewall on the server machine allows incoming connections on the specified port. You may need to create a rule to allow traffic on port 9999.
- Static IP or Dynamic DNS: If the server is hosted on a home network, consider using a static IP address or a Dynamic DNS service to make connecting easier for clients.

