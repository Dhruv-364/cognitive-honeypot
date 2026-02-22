import socket
import threading
import paramiko
import json
from datetime import datetime, UTC
import os

HOST_KEY = paramiko.RSAKey.generate(2048)

LOG_FILE = "data/ssh_logs.jsonl"
os.makedirs("data", exist_ok=True)

def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(event) + "\n")

class FakeSSHServer(paramiko.ServerInterface):
    def __init__(self, client_ip):
        self.event = threading.Event()
        self.client_ip = client_ip

    def check_auth_password(self, username, password):
        log_event({
            "time": datetime.now(UTC).isoformat(),
            "ip": self.client_ip,
            "username": username,
            "password": password,
            "type": "ssh_login"
        })
        return paramiko.AUTH_SUCCESSFUL # type: ignore

    def get_allowed_auths(self, username):
        return "password"

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED # type: ignore
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED # type: ignore

    def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
        return True

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True


def handle_client(client, addr):
    transport = paramiko.Transport(client)
    transport.add_server_key(HOST_KEY)

    server = FakeSSHServer(addr[0])

    try:
        transport.start_server(server=server)
    except Exception:
        transport.close()
        return

    chan = transport.accept(20)
    if chan is None:
        transport.close()
        return

    chan.send(b"Welcome to Ubuntu 20.04 LTS\n")
    chan.send(b"$ ")

    buffer = ""

    try:
        while True:
            data = chan.recv(1024)
            if not data:
                break

            buffer += data.decode("utf-8", errors="ignore")

            # Process line by line (Enter key)
            while "\n" in buffer or "\r" in buffer:
                line, _, buffer = buffer.partition("\n")
                command = line.strip()

                if command == "":
                    chan.send(b"$ ")
                    continue

                log_event({
                    "time": datetime.now(UTC).isoformat(),
                    "ip": addr[0],
                    "command": command,
                    "type": "ssh_command"
                })

                if command in ["exit", "quit"]:
                    chan.send(b"logout\n")
                    chan.close()
                    transport.close()
                    return

                if command == "ls":
                    chan.send(b"config.txt  users.db  backup.sql\n")
                elif command == "whoami":
                    chan.send(b"root\n")
                elif command == "pwd":
                    chan.send(b"/root\n")
                else:
                    chan.send(b"command not found\n")

                chan.send(b"$ ")
    except Exception:
        pass

    chan.close()
    transport.close()


def start_ssh_honeypot(host="0.0.0.0", port=2222):
    print(f"🚨 SSH Honeypot running on port {port}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(100)

    while True:
        client, addr = sock.accept()
        print(f"[+] Connection from {addr[0]}")
        t = threading.Thread(target=handle_client, args=(client, addr), daemon=True)
        t.start()


if __name__ == "__main__":
    start_ssh_honeypot()