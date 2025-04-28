# server.py
import socket, threading
from encryption_utils import encrypt, decrypt
from logger_utils import log_message

clients = {}     # username: (socket, addr)
lock = threading.Lock()

def broadcast(data: bytes, exclude_sock=None):
    with lock:
        for user, (sock, _) in clients.items():
            if sock is not exclude_sock:
                try:
                    sock.sendall(data)
                except:
                    pass

def send_user_list():
    users = list(clients.keys())
    payload = f"USERS:{','.join(users)}".encode('utf-8')
    broadcast(encrypt(payload))

def handle_client(sock, addr):
    try:
        raw = sock.recv(4096)
        username = decrypt(raw).decode()
        with lock:
            clients[username] = (sock, addr)
        print(f"{username} connected")
        broadcast(encrypt(f"🟢 {username} joined".encode()))
        send_user_list()

        while True:
            packet = sock.recv(8192)
            if not packet: break

            data = decrypt(packet)
            if data.startswith(b"TYPING:"):
                # TYPING:user1:START or STOP
                broadcast(encrypt(data), exclude_sock=sock)
            elif data.startswith(b"FILE:"):
                # FILE:filename:filesize:<binary...>
                broadcast(encrypt(data), exclude_sock=sock)
                log_message(f"[FILE] {username} sent a file")
            else:
                msg = data.decode()
                log_message(msg)
                broadcast(encrypt(data), exclude_sock=sock)

    except Exception as e:
        print("Error:", e)
    finally:
        with lock:
            for user, (csock, _) in list(clients.items()):
                if csock is sock:
                    del clients[user]
                    broadcast(encrypt(f"🔴 {user} left".encode()))
                    break
        send_user_list()
        sock.close()

def start_server(host='0.0.0.0', port=12345):
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.bind((host, port))
    srv.listen(10)
    print("Server listening…")
    try:
        while True:
            csock, addr = srv.accept()
            threading.Thread(target=handle_client, args=(csock, addr), daemon=True).start()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()

if __name__ == "__main__":
    start_server()
