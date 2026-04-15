import socket
import threading

HOST = "0.0.0.0"
PORT = 25565
ROOM_PASSWORD = "1234"

clients = []

def handle_client(client, addr):
    try:
        client.send("Введите пароль комнаты: ".encode())
        password = client.recv(1024).decode().strip()

        if password != ROOM_PASSWORD:
            client.send("Неверный пароль!\n".encode())
            client.close()
            return

        client.send("Введите ник: ".encode())
        nickname = client.recv(1024).decode().strip()

        welcome = f"{nickname} подключился!\n"
        print(welcome)

        broadcast(welcome, client)
        clients.append((client, nickname))

        while True:
            message = client.recv(1024)
            if not message:
                break

            text = f"{nickname}: {message.decode()}"
            print(text)
            broadcast(text, client)

    except:
        pass
    finally:
        remove_client(client)


def broadcast(message, sender):
    for client, _ in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                remove_client(client)


def remove_client(client):
    for c, nick in clients:
        if c == client:
            clients.remove((c, nick))
            print(f"{nick} отключился")
            broadcast(f"{nick} вышел\n", client)
            break
    client.close()


def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Сервер запущен на {HOST}:{PORT}")

    while True:
        client, addr = server.accept()
        print(f"Подключение: {addr}")

        thread = threading.Thread(target=handle_client, args=(client, addr))
        thread.start()


start()