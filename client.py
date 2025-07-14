# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
from random import randint

HOST = '127.0.0.1'
PORT = 1234
PEER_PORT = randint(1000, 5000)

DARK_GREY = '#121212'
MEDIUM_GREY = '#1F1B24'
OCEAN_BLUE = '#464EB8'
WHITE = "white"
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)


# Creating a socket object
# AF_INET: we are going to use IPv4 addresses
# SOCK_STREAM: we are using TCP packets for communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
peer_c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pc = None 
addr2 = None 

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)



def peer_ready_to_connect():
    global pc, addr2
    peer_s.bind((HOST, PEER_PORT))
    peer_s.listen()
    pc, addr2 = peer_s.accept()
    print("connected to peer!")
    add_message(f"Connected to Peer: {addr2}")
    print(pc, addr2)
    #pc.sendall("Hello 2".encode())
    threading.Thread(target=send_message, ).start()
    threading.Thread(target=recv_comm_peer, args=(pc, )).start()

def comm_peer(pc):
    #pc.sendall("Hello jvfjhvf".encode())
    message = message_textbox.get()
    if "to_peer" in message: 
        pc.sendall(message.encode())

def recv_comm_peer(pc):
    while 1:
        message = pc.recv(2048).decode('utf-8')
        message = message.split(":")[1]
        add_message(f"[From Peer]: {message}")   
        print(message)


def connect():

    # try except block
    try:

        # Connect to the server
        print("my peer port", PEER_PORT )
        client.connect((HOST, PORT))
        threading.Thread(target=peer_ready_to_connect, args=( )).start()
        print("Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
        add_message("my peer port", PEER_PORT)
    except:
        pass 

    username = username_textbox.get()
    username += f";peer_port={PEER_PORT}"
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)





def send_message():
    global pc
    message = message_textbox.get()
    if "to_peer" in message: 
        if pc == None:
            peer_c.sendall(message.encode())
        else: 
            pc.sendall(message.encode())

    elif 'conn' in message: 
        h = message.split(":")[1]
        p = message.split(":")[2]
        p = int(p)
        peer_c.connect((HOST,p))
        print("connected")
        add_message(f"Connected to Peer!")
        #peer_c.sendall("hello".encode())
        threading.Thread(target=comm_peer, args=(peer_c, )).start()
        threading.Thread(target=recv_comm_peer, args=(peer_c, )).start()    

    elif message != '':
        if "close" in message:
            add_message("Connection close! You may close the window.")
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    
        
    else:
        pass

root = tk.Tk()
root.geometry("600x600")
root.title("Messenger Client")
root.resizable(False, False)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=MEDIUM_GREY)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=DARK_GREY)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_GREY, fg=WHITE)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=MEDIUM_GREY, fg=WHITE, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=OCEAN_BLUE, fg=WHITE, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=MEDIUM_GREY, fg=WHITE, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)


def listen_for_messages_from_server(client):
    while 1:
        message = client.recv(2048).decode('utf-8')
        add_message(f"{message}")


            

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()