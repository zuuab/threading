#!/usr/bin/env python3
import socket

def run_client():
    # create the socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # server details
    server_ip = "127.0.0.1"
    server_port = 8000

    # establish connection with the server
    client.connect((server_ip, server_port))

    try:
        while True:
            # input message and send it to the server
            msg = input("Enter message: ")
            # example, so we will trim to 1024 bytes as a max
            client.send(msg.encode("utf-8")[:1024])

            # receive message back from the server
            response = client.recv(1024)
            response = response.decode("utf-8")

            # if server sent us "closed" then break the loop and close the socket
            if response.lower() == "closed":
                break
            print(f"Received: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # closes client socket
        client.close()
        print(f"Connection to server ({server_ip}) closed")

run_client()