from copyreg import pickle
import socket
from urllib import response
import pickle

hostPort = '127.0.0.1'
port = 2121

ADR = (hostPort, port)
BUFF = 2048
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def control_Chanel():
    try:
        client.connect(ADR)
    except:
        print("failed to connect!\ntry again?\n")
        ans = input("yes/no : ")
        if ans == "yes":
            control_Chanel()
        elif ans == "no":
            print("As you wish...")
            Help()
            return
    print("Connection stabilised\n")


def List(order):
    ##order = "list"
    client.send(order.encode())

    responce = client.recv(BUFF)
    recList = pickle.loads(responce)
    for item in recList:
        print(item)


def download(order):  # cherte bayad dorost she
    rand_port = client.recv(BUFF).decode()

    if rand_port == "404":
        print("Error 404!!!\nFile not found\n")
    else:
        tmp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tmp_client.connect((hostPort, int(rand_port)))

        data = b""
        download_b = tmp_client.recv(1048576)
        data += download_b

        my_file = "downloaded " + order[5:]
        with open(my_file, 'wb') as file:
            file.write(data)

        print(order[5:] + " Downloaded successfully")
        tmp_client.close()


def pwd(order):
    ##order = "pwd"

    client.send(order.encode())
    responce = client.recv(BUFF).decode()
    if responce.find('myServer') != -1:
        print(responce[responce.find('myServer'):])
    else:
        print(responce)


def change_dir(order):
    ##order = "cd"
    client.send(order.encode())
    responce = client.recv(BUFF).decode()
    if responce.find('myServer') != -1:
        print(responce[responce.find('myServer'):])
    else:
        print(responce)


def Exit(order):
    client.send(order.encode())
    responce = client.recv(BUFF).decode()
    print(responce)
    exit(0)


def stepBack(order):
    client.send(order.encode())
    responce = client.recv(BUFF).decode()
    if responce.find('myServer') != -1:
        print(responce[responce.find('myServer'):])
    else:
        print(responce)


def Help():
    while True:
        print('###############################')
        print("What can we do for you???")
        print("Help\nList(this will help you to get list of files)\nDWLD(this will help you download a file)\nPWD")
        print("CD(change directory)\nExit")

        answer = input("Answer : ")
        if answer.lower().find("help") != -1:
            Help()
        elif answer.lower().find("list") != -1:
            List(answer)
        elif answer.lower().find("dwld") != -1:
            client.send(answer.encode())
            download(answer)
        elif answer.lower().find("pwd") != -1:
            pwd(answer)
        elif answer.lower().find("cd") != -1:
            change_dir(answer)
        elif answer.lower() == "exit":
            Exit(answer)
        elif answer == '..':
            stepBack(answer)
        else:
            print("Command not available!")


if __name__ == "__main__":
    print("Howdy!!!")
    print("Welcome to simple FTP-Protocol developed by Pouya and amir\n")
    control_Chanel()
    Help()