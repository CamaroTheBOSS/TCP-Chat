# TCP-Chat
Implementation of simple TCP/IP communication between multiple clients indirectly via the server

SERVER:
Server works on threads. Each thread serves a different (server, client) connection. One main thread collects all new connections. All the connections are stored
in global list. Because of that each thread can broadcast message from its client to all the other clients.

CLIENT:
Client works on threads as well. One thread is responsible for writing to server, second one is responsible for reading from server. It gives us possibility to communicate with another clients asynchronously (console locking not occur). In addition it is possible to send .doc file with command sendDoc nameOfFile.doc.

MAIN.PY:
This is simple script for fast turning on the cmd consoles with clients and server. It is possible to connect multiple clients without any limit
