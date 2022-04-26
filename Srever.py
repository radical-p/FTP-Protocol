from os import listdir
from socket import *
from genericpath import getsize, isdir
from os.path import isfile, join
import os
import pickle
import random

Server = '127.0.0.1'
Port = 2121
BUFF = 2048
try:
    server = socket(AF_INET, SOCK_STREAM)
    server.bind((Server, Port))
    server.listen(5)
    print("Connection Stabilized")
except:
    print("Couldn't create channel!")
    exit(0)

DirectoryLevel = os.getcwd()

connectionSocket, add = server.accept()
while True:

    order = connectionSocket.recv(BUFF).decode()

    print("received order is :" + order)
    if (order == 'list'):
        lsDir = listdir(DirectoryLevel)
        # connectionSocket.send(str(len(lsDir)).encode('UTF-8'))
        sendLs = []
        if (lsDir):
            sumSize = 0
            for dir in lsDir:
                if (isdir(join(DirectoryLevel, dir))):
                    myStr = '[]\t' + dir + '\t' + str(getsize(join(DirectoryLevel, dir)))
                    print(myStr)
                    sendLs.append(myStr)
                else:
                    myStr = '  \t' + dir + '\t' + str(getsize(join(DirectoryLevel, dir)))
                    print(myStr)
                    sendLs.append(myStr)

                sumSize += getsize(join(DirectoryLevel, dir))

            sendLs.append('sum : \t\t\t' + str(sumSize))
            data = pickle.dumps(sendLs)
            connectionSocket.send(data)

        else:
            print('no directory here')
            connectionSocket.send('no directory here'.encode())

            # cd server code
    elif (order.find("cd") != -1):
        newDir = order[order.find(' ') + 1:]
        onlyfiles = [f for f in listdir(DirectoryLevel) if isdir(join(DirectoryLevel, f))]
        currentDir = False

        for x in onlyfiles:
            if (x == newDir):
                currentDir = True

        if (currentDir):
            DirectoryLevel += '/'
            DirectoryLevel += newDir
            print('success action (CD)')
            connectionSocket.send((DirectoryLevel).encode())
            os.chdir(DirectoryLevel)
        else:
            print('directory NOT FOUND !')
            connectionSocket.send(('directory NOT FOUND !').encode())

            # pwd server code
    elif order.find("pwd") != -1:
        print(DirectoryLevel)
        connectionSocket.send(DirectoryLevel.encode())

    elif order == 'exit':
        print('client left the connection ;)')
        connectionSocket.send('Goodbye'.encode())
        break
    elif order == '..':  # step back
        temp = DirectoryLevel[:DirectoryLevel.rfind('/')]

        if (temp.find('myServer') != -1):
            print('success action (CD ..)')
            DirectoryLevel = temp
            print(DirectoryLevel)
            connectionSocket.send(DirectoryLevel.encode())
        else:
            print('Bad access request denied')
            connectionSocket.send('Bad request'.encode())
    # DWLD server code
    elif order.lower().find("dwld") != -1:
        file_name = order[5:]

        random_port = random.randint(3000, 50000)
        tmp_socket = socket(AF_INET, SOCK_STREAM)
        tmp_socket.bind((Server, random_port))
        tmp_socket.listen(5)

        if file_name in os.listdir():
            print()
            print(os.listdir())
            print()
            print("trying to download " + file_name)

            connectionSocket.send(str(random_port).encode())
            tmp_connection, tmp_address = tmp_socket.accept()

            if os.path.exists(file_name):
                print("Download started...")
                with open(file_name, 'rb') as f:
                    data = f.read()
                    tmp_connection.send(data)
            tmp_socket.close()
            print("Download completed")
        else:
            print("Bad request!!!")
            connectionSocket.send(str(404).encode())


connectionSocket.close()