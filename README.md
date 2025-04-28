Local Network Chat Application
A simple chat application built with Python and PyQt for local network communication. This app allows users to chat with each other within a local network by connecting to a server.

Features
User login and nickname selection

Real-time messaging

Simple and clean user interface

Resizable window for dynamic user experience

Server-client architecture (server.py handles connections and client communication)

Requirements
To run this application, you need to have the following installed:

Python 3.x (Recommended: Python 3.8 or above)

PyQt5 for the graphical user interface (GUI)

Cryptography for secure data encryption

You can install the dependencies using pip:

bash
pip install -r requirements.txt

or

bash
pip install pyqt5 cryptography
Setup
Clone this repository or download the source code.

Install the required dependencies:

bash

pip install pyqt5 cryptography
You will need to run the server and the client:

Server: Start the server by running server.py on the machine that will host the server.

bash

python server.py
Client: Start the client by running gui.py on the client machines.

bash

python gui.py
After starting the server, the client can connect by entering a valid nickname and starting the chat.

## Deployment (Packaging as Executable)
You can package this application into a standalone executable using PyInstaller.

# Install PyInstaller:

bash

pip install pyinstaller
Create an executable for the client by running:

bash

pyinstaller --onefile --windowed gui.py
After packaging, you can find the executable in the dist/ directory. You can distribute this .exe (for Windows) or the equivalent for other platforms.

# Usage
Running the Server: On the machine that will act as the server, start the server by running:

bash
python server.py
Running the Client: On the client machines, run:

bash
python gui.py
The client will prompt you to enter a nickname, and once entered, you can start chatting with other clients connected to the server.

Message Sending: Type your message in the text input field and click "Send" to send it to others on the local network.

Troubleshooting
No Connection to Server: Ensure that both the server and client are on the same local network and that the server is running before the client connects.

Encryption Issues: Make sure that the correct encryption key is set up in the server and client scripts for secure communication.