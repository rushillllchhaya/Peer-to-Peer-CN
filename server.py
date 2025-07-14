# Import required modules
import socket
import threading

HOST = '127.0.0.1'
PORT = 1234 
LISTENER_LIMIT = 5
active_clients = [] # List of all currently connected users


def listen_for_messages(client, addr):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message == "server_close":
            
            send_messages_to_all(f"Peer has left: {addr[0]} {addr[1]}")
            print(f"Peer has left: {addr[0]} {addr[1]}")
            active_clients.remove((addr, client))
            print(f"Number of active peers: ", len(active_clients))
            client.close()
            break




# Function to send message to a single client
def send_message_to_client(client, message):
    client.sendall(message.encode())

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    for user in active_clients:
        send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client, addr):
    
    # Server will listen for client message that will
    # Contain the username
    while 1:

        username = client.recv(2048).decode('utf-8')
        if username != '':
            peer_port = username.split(';')[1][8:]
            active_clients.append((addr, client))
            print(f"New peer joined:  {addr[0]} {addr[1]}", f"Peer port: {peer_port}")
            print(f"Number of active peers: ", len(active_clients))
            prompt_message = f"New peer joined:  {addr[0]} {addr[1]}" +  f"Peer port: {peer_port}"
            prompt_message += "\nTotal connected Clients: "
            for x in active_clients:
                prompt_message += f"\n{x[0][0]} {x[0][1]}"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
    threading.Thread(target=listen_for_messages, args=(client, addr)).start()

# Main function
def main():

    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")

    # Set server limit
    server.listen()

    # This while loop will keep listening to client connections
    while 1:

        client, address = server.accept()
        threading.Thread(target=client_handler, args=(client, address)).start()


if __name__ == '__main__':
    main()

