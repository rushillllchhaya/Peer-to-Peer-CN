# Peer-to-Peer-CN: Simple Peer-to-Peer Messaging System

This repository contains a basic peer-to-peer messaging system implemented in Python, designed for the Computer Networks subject. It allows two or more computers within the same network to communicate with each other through a central server, which facilitates the initial connection and message routing.

## Project Overview

This system demonstrates fundamental concepts of network programming, including socket programming, multi-threading, and client-server communication, extended to support peer-to-peer messaging. The central server acts as a rendezvous point, helping clients discover each other before direct peer-to-peer communication can be established.

## Functionality

- **Central Server (`server.py`)**: Manages client connections, registers active clients, and relays initial connection information between peers. It keeps track of connected clients and their respective peer ports.
- **Client Application (`client.py`)**: A GUI-based client (using `tkinter`) that allows users to:
    - Connect to the central server.
    - Send messages to other connected peers.
    - Receive messages from other peers.
    - Initiate direct peer-to-peer connections.

## How it Works

1.  **Server Startup**: The `server.py` script is started first. It listens for incoming client connections on a predefined IP address and port.
2.  **Client Connection**: Each `client.py` instance connects to the central server. Upon connection, the client sends its username and a randomly generated peer port to the server.
3.  **Peer Discovery**: The server informs all connected clients about new peers joining the network, including their IP addresses and peer ports.
4.  **Peer-to-Peer Communication**: Clients can then use the information provided by the server to establish direct connections with other peers. Once a direct connection is established, messages are exchanged directly between the peers, bypassing the central server for actual message content.

## File Structure

- `server.py`: The Python script for the central server.
- `client.py`: The Python script for the client application with a Tkinter GUI.

## Requirements

To run this peer-to-peer messaging system, you will need Python 3.x installed. The following Python libraries are required:

- `socket` (built-in)
- `threading` (built-in)
- `tkinter` (built-in)
- `random` (built-in)

No external installations are typically needed for these standard libraries.

## Setup and Usage

Follow these steps to set up and run the peer-to-peer messaging system:

### 1. Clone the Repository

```bash
git clone https://github.com/rushillllchhaya/Peer-to-Peer-CN.git
cd Peer-to-Peer-CN
```

### 2. Start the Server

Open a terminal or command prompt and run the server script:

```bash
python server.py
```

The server will start listening for connections on `127.0.0.1:1234` (localhost).

### 3. Start Client Applications

Open one or more separate terminals or command prompts for each client you want to run. For each client, navigate to the `Peer-to-Peer-CN` directory and run the client script:

```bash
python client.py
```

Each client will open a GUI window. Enter a username and click "Join" to connect to the server. The client will also open a random port for peer-to-peer communication.

### 4. Communicate Between Peers

- **Server Messages**: The server will display messages when new peers join or leave.
- **Client Messages**: In the client GUI:
    - To send a message to the server (and thus broadcast to all connected clients), type your message in the input box and click "Send".
    - To connect to a specific peer, use the format `conn:<peer_ip>:<peer_port>`. For example, if a peer is at `127.0.0.1` and its peer port is `3456`, you would type `conn:127.0.0.1:3456` and press Send. The peer port is displayed in the client's message box when it connects to the server.
    - To send a message directly to a connected peer, use the format `to_peer:<your_message>`. For example, `to_peer:Hello there!`.
    - To close your client connection, type `close` and click "Send".

**Note**: For communication between different PCs on the same network, replace `127.0.0.1` with the actual IP address of the machine running the server and the respective peer. Ensure that firewalls are configured to allow connections on the specified ports (`1234` for the server and the randomly generated peer ports for clients).
