import socket
import os

SERVER_IP = "10.194.40.15"
SERVER_PORT = 5555

ENTRY_NUMBER = "2024JCS2611"


def main():
    server_address = (SERVER_IP, SERVER_PORT)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)
            s.sendall(ENTRY_NUMBER.encode())
            public_key = s.recv(1024).decode()
            public_key_parts = public_key.split(',')
            P = int(public_key_parts[0])
            Q = int(public_key_parts[1])
            print(f"P = {P}, Q = {Q}")
    except Exception as e:
        print(f"Failed to connect to server: {e}")


if __name__ == "__main__":
    main()
