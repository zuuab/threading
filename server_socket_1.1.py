#!/usr/bin/env python3
import socket
import threading

def handle_client(client_socket, addr):
    try:
        while True:
            # receive and print client messages
            request = client_socket.recv(1024).decode("utf-8")
            if request.lower() == "close":
                client_socket.send("closed".encode("utf-8"))
                break
            print(f"Received: {request}")
            # convert and send accept response to the client
            response = "accepted"
            client_socket.send(response.encode("utf-8"))
    except Exception as e:
        print(f"Error when hanlding client: {e}")
    finally:
        client_socket.close()
        print(f"Connection to client ({addr[0]}:{addr[1]}) closed")
        
def run_server():
    server_ip = "127.0.0.1"
    port = 8000
    try:
        # create a socket object
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind server socket to an IP address and port
        server.bind((server_ip, port))

        # listen for incoming connections
        server.listen()
        print(f"Listening on {server_ip}:{port}")

        # receive data from the client
        while True:
            # accept incoming connections
            client_socket, client_address = server.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

            thread = threading.Thread(target=handle_client, args=(client_socket, client_address,))
            thread.start()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        server.close()

run_server()