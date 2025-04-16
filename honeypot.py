import socket
import threading
import datetime

def log_connection(ip, port, data):
    with open("log.txt", "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] Connection from {ip}:{port} - Data: {data}\n")

def handle_client(client_socket, address):
    try:
        data = client_socket.recv(1024).decode(errors="ignore")
        log_connection(address[0], address[1], data.strip())
        response = "Access denied.\n"
        client_socket.send(response.encode())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

def start_honeypot(host='0.0.0.0', port=2222):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[+] Honeypot listening on {host}:{port}...")

    while True:
        client_socket, addr = server.accept()
        print(f"[!] Incoming connection from {addr[0]}:{addr[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

if __name__ == "__main__":
    start_honeypot()

