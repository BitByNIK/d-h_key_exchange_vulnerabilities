import random
import socket

SERVER_IP = "10.194.40.15"
SERVER_PORT = 5555

ENTRY_NUMBER = "2024JCS2611"


def main():
    server_address = (SERVER_IP, SERVER_PORT)
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(server_address)
            s.sendall(ENTRY_NUMBER.encode())
            dh_parameters = s.recv(1024).decode().split(',')
            P = int(dh_parameters[0])
            G = int(dh_parameters[1])
            print(f"P = {P}, G = {G}")

            private_key = random.getrandbits(32)
            print(f"Private Key of {ENTRY_NUMBER}: {private_key}")

            public_key = pow(G, private_key, P)
            s.sendall(str(public_key).encode())
            print(f"Public Key of {ENTRY_NUMBER}: {public_key}")

            shared_secret = pow(int(s.recv(1024).decode()), private_key, P)
            print(f"Shared Secret: {shared_secret}")

            private_key_server = 1
            while (True):
                if shared_secret == pow(G, private_key * private_key_server, P):
                    print(f"Private Key of Server: {private_key_server}")
                    break
                private_key_server += 1

    except Exception as e:
        print(f"Failed to connect to server: {e}")


if __name__ == "__main__":
    main()
