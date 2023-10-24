#!/usr/bin/env python3
import socket

def run_server():
    # AF_INET is IPv4, AFINET6 is IPv6, AF_UNIX for Unix-sockets
    # SOCK_STREAM indicates a TCP socket, SOCK_DGRAM indicates UDP
    # RAW_SOCKET will require you to create all of the protocols yourself instead of allowing the operating system to handle it
    # create a socket object
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # binding server socket to an IP address and port
    server_ip = "127.0.0.1"
    port = 8000
    server.bind((server_ip, port))

    # listen for incoming connections
    # the number indicates the size of backlog you will allow, in this case only one connection can happen at a time
    # If you omit the backlog argument, it will be set to your system’s default (under Unix, you can typically view this default in the /proc/sys/net/core/somaxconn file).
    server.listen(0)
    print(f"Listening on {server_ip}: {port}")

    # accept incoming connections
    # accept will stall the execution thread until a client connects. Then returns a tuple pair of (conn, address) of the client's IP and port. conn becomes a new socket object
    client_socket, client_address = server.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # receive data from the client
    # recv: recieves the specified number of bytes from the client
    # decode: transforms the binary data into a string
    while True:
        request =client_socket.recv(1024)
        request = request.decode("utf-8")

        # if "close" from the client then we break the loop and close the connection
        if request.lower() == "close":
            # this sends a response to the client that the connection should be closed then breaks the loop
            client_socket.send("closed".encode("utf-8"))
            break

        print(f"Received: {request}")

        response = "accepted".encode("utf-8")
        client_socket.send(response)
    
    # close connection socket with the client
    client_socket.close()
    print("Connection to the client closed")
    server.close()

run_server()