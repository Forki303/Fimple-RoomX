import socket
import threading

SERVER_IP = input("IP сервера: ")
PORT = int(input("Порт: "))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, PORT))


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Ошибка подключения")
            client.close()
            break


def send():
    while True:
        message = input()
        client.send(message.encode())


threading.Thread(target=receive).start()
threading.Thread(target=send).start()