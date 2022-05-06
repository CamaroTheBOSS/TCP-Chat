import socket
import threading

HEADER = 8        # 8 bytes for message's length
MESSAGE_TYPE = 2  # 2 bytes for message's type

PORT = 5050
# SERVER = socket.gethostbyname(socket.gethostname())  # Creates server on IP gave by the computer we turn on the script
SERVER = "127.0.0.1"  # localhost
ADDRESS = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)
connections = []


def reSend(conn, message):
    message = message.encode(FORMAT)
    length = str(len(message)).encode(FORMAT)
    length += b' ' * (HEADER - len(length))
    conn.send(length)
    conn.send(message)


def handleClient(conn, address):
    try:
        print(f"[NEW CONNECTION] {address}")
        connected = True
        connections.append(conn)
        while connected:
            header = conn.recv(HEADER + MESSAGE_TYPE).decode(FORMAT)  # This line is blocking further code
            if header:
                # length of the message is the header minus two bits of prefix (message type)
                messageType = int(header[:MESSAGE_TYPE])
                length = int(header[MESSAGE_TYPE:])
                message = conn.recv(length).decode(FORMAT)
                if messageType == 0:
                    if message == DISCONNECT_MESSAGE:
                        connected = False
                    print(f"[MESSAGE FROM {address}]: {message}")
                    for connection in connections:
                        reSend(connection, message)
                elif messageType == 1:
                    print(f"[MESSAGE FROM {address}]: {message}")
                    for connection in connections:
                        reSend(connection, message)

    except ConnectionResetError:
        connected = False
        print(f"[MESSAGE FROM {address}]: {DISCONNECT_MESSAGE}")
    if conn in connections:
        connections.remove(conn)


# Here is the server main loop:
# Server waits for new connections in server.accept() (code is blocked)
# After detecting new connection it is creating new thread which will be serving this connection
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, address = server.accept()  # This line is blocking further code
        thread = threading.Thread(target=handleClient, args=(conn, address))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print("[STARTING] Server is starting...")
start()