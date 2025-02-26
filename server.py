import socket
import threading
clients = []
nicknames = []
def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f"{nickname} left the chat.".encode("utf-8"))
            nicknames.remove(nickname)
            break
def receive():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1", 55555))
    server.listen()
    while True:
        client, address = server.accept()
        client.send("NICK".encode("utf-8"))
        nickname = client.recv(1024).decode("utf-8")
        nicknames.append(nickname)
        clients.append(client)
        broadcast(f"{nickname} joined the chat!".encode("utf-8"))
        client.send("Connected to the server!".encode("utf-8"))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print("Server running...")
receive()
