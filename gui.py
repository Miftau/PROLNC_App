# gui.py
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit,
    QPushButton, QListWidget, QFileDialog, QListWidgetItem, QLabel, QComboBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from client import ChatClient

EMOJIS = ["😀","😂","😍","👍","🎉","😢","😡"]

class ChatWindow(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.setWindowTitle(f"{username} — PROGRESS LAN Chat App")
        self.resize(700, 450)
        self.setup_ui()
        self.client = ChatClient(
            username=username,
            on_message=self.append_message,
            on_userlist=self.update_user_list,
            on_typing=self.show_typing,
            on_file=self.receive_file
        )
        self.client.connect()

    def setup_ui(self):
        main = QVBoxLayout(self)

        # Top area: messages + users
        top = QHBoxLayout()
        self.chat = QTextEdit(readOnly=True)
        top.addWidget(self.chat, 3)
        self.users = QListWidget()
        top.addWidget(self.users, 1)
        main.addLayout(top)

        # Typing indicator
        self.typing_label = QLabel("")
        main.addWidget(self.typing_label)

        # Bottom area: emoji, input, send, file
        bottom = QHBoxLayout()
        self.emoji_picker = QComboBox()
        self.emoji_picker.addItems(EMOJIS)
        self.emoji_picker.currentIndexChanged.connect(
            lambda i: self.msg_input.insert(EMOJIS[i])
        )
        bottom.addWidget(self.emoji_picker)

        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Type your message...")
        self.msg_input.textEdited.connect(self.on_text_edited)
        self.msg_input.returnPressed.connect(self.send_message)
        bottom.addWidget(self.msg_input, 3)

        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        bottom.addWidget(self.send_btn)

        self.file_btn = QPushButton("📎")
        self.file_btn.clicked.connect(self.send_file)
        bottom.addWidget(self.file_btn)

        main.addLayout(bottom)

        # typing timeout
        self._typing_timer = QTimer(self)
        self._typing_timer.setInterval(2000)
        self._typing_timer.timeout.connect(lambda: self.client.send_typing(False))

    def on_text_edited(self):
        self.client.send_typing(True)
        self._typing_timer.start()

    def send_message(self):
        text = self.msg_input.text().strip()
        if not text: return
        self.client.send(text)
        self.msg_input.clear()

    def send_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select File")
        if path:
            self.append_message(f"📎 You sent file: {os.path.basename(path)}")
            self.client.send_file(path)

    def receive_file(self, data: bytes):
        # data starts with b"FILE:fname:size:"
        header, _, rest = data.partition(b':')  # crude split
        _, fname, size = header.decode().split(':')
        save_path = os.path.join(os.getcwd(), fname)
        with open(save_path, 'wb') as f:
            f.write(rest)  # in real app, handle chunking, filesize, etc.
        self.append_message(f"📎 Received file: {fname} (saved)")

    def append_message(self, msg: str):
        self.chat.append(msg)

    def update_user_list(self, users):
        self.users.clear()
        for u in users:
            item = QListWidgetItem(u)
            # Simple status icon: green dot for self, gray for others
            icon = QIcon("icons/green.png") if u in users else QIcon("icons/gray.png")
            item.setIcon(icon)
            self.users.addItem(item)

    def show_typing(self, user, is_typing):
        if is_typing and user != self.username:
            self.typing_label.setText(f"{user} is typing…")
        else:
            self.typing_label.setText("")

    def closeEvent(self, e):
        self.client.close()
        e.accept()

