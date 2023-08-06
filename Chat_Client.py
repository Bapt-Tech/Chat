import socket
import threading
import re

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Entrez l'adresse IP du serveur : ")
    client.connect((server_ip, 12345))

    username = input("Choisissez un nom d'utilisateur : ")
    client.send(username.encode('utf-8'))

    while True:
        message = client.recv(1024).decode('utf-8')
        print(message)
        if "Choisissez un salon" in message:
            selected_channel = input()
            client.send(selected_channel.encode('utf-8'))
        else:
            break

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input()
        if message.lower() == '/exit':
            client.send(message.encode('utf-8'))
            break
        elif message.startswith('/join'):
            new_channel = message.split()[1]
            client.send(f"/join {new_channel}".encode('utf-8'))
        elif message.startswith('@'):
            recipient, _, message = message.partition(' ')
            recipient = recipient[1:]  # Supprimer le @ du nom d'utilisateur du destinataire
            client.send(f"@{recipient} {message}".encode('utf-8'))
        elif not message.startswith('/'):
            client.send(message.encode('utf-8'))

    print("Vous avez quitté le chat.")
    client.close()

def receive_messages(client):
    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            print(message)
    except:
        print("Connexion perdue avec le serveur")
        client.close()

if __name__ == "__main__":
    start_client()
