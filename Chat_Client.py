import socket
import threading
import re
from time import sleep

def RetryClientToServerConnexion():
    try:
        print("Une Erreur s'est déclenchée...")
        print("Reconnexion dans 10 secondes...")
        print("Vous devrez probablement vous reconnecter")
        print("10")
        sleep(1)
        print("9")
        sleep(1)
        print("8")
        sleep(1)
        print("7")
        sleep(1)
        print("6")
        sleep(1)
        print("5")
        sleep(1)
        print("4")
        sleep(1)
        print("3")
        sleep(1)
        print("2")
        sleep(1)
        print("1")
        sleep(1)
        print("Retry...")
        start_client()
    except ConnexionResetError:
        RetryClientToServerConnexion()
    

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
        try:
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
            elif message.lower() == '/salonlist':
                client.send(message.encode('utf-8'))
            elif message.lower() == '/users':
                client.send(message.encode('utf-8'))
            elif not message.startswith('/'):
                client.send(message.encode('utf-8'))
        except ConnectionResetError:
            RetryClientToServerConnexion()

    print("Vous avez quitté le chat.")
    client.close()

def receive_messages(client):
    try:
        while True:
            message = client.recv(1024).decode('utf-8')
            print(message)

    except ConnectionResetError:
        RetryClientToServerConnexion()

    except:
        print("Connexion perdue avec le serveur")
        client.close()



if __name__ == "__main__":
    start_client()
