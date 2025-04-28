# client.py
import socket, threading, os
from encryption_utils import encrypt, decrypt

class ChatClient:
    def __init__(self, username, host='127.0.0.1', port=12345,
                 on_message=None, on_userlist=None, on_typing=None, on_file=None):
        self.username = username
        self.on_message = on_message
        self.on_userlist = on_userlist
        self.on_typing = on_typing
        self.on_file = on_file
        self.sock = socket.socket()
        self.running = True
        self.host, self.port = host, port

    def connect(self):
        self.sock.connect((self.host, self.port))
        self.sock.sendall(encrypt(self.username.encode()))
        threading.Thread(target=self.listen, daemon=True).start()

    def send(self, text: str):
        data = text.encode('utf-8')
        self.sock.sendall(encrypt(data))

    def send_typing(self, start: bool):
        flag = "START" if start else "STOP"
        payload = f"TYPING:{self.username}:{flag}".encode()
        self.sock.sendall(encrypt(payload))

    def send_file(self, filepath: str):
        fname = os.path.basename(filepath)
        size = os.path.getsize(filepath)
        header = f"FILE:{fname}:{size}:".encode()
        self.sock.sendall(encrypt(header))
        with open(filepath, 'rb') as f:
            while chunk := f.read(4096):
                self.sock.sendall(encrypt(chunk))

    def listen(self):
        while self.running:
            packet = self.sock.recv(8192)
            if not packet:
                break
            data = decrypt(packet)
            text = data.decode(errors='ignore')
            if text.startswith("USERS:"):
                self.on_userlist(text.replace("USERS:", "").split(','))
            elif text.startswith("TYPING:"):
                _, user, flag = text.split(':',2)
                self.on_typing(user, flag=="START")
            elif text.startswith("FILE:"):
                # FILE handling delegated to GUI callback
                self.on_file(data)
            else:
                self.on_message(text)

    def close(self):
        self.running = False
        self.sock.close()
