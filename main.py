#!/usr/bin/env python3

import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    # Main Function
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        shop = False
        self.gold = 100
        self.weapon = 0
        self.welcome()
        self.info()
        self.main_menu()
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode("UTF-8").rstrip()
            if (not data) or (msg == "bye"):
                self.csocket.send(bytes("Your connection will be closed. Please reconnect!",'UTF-8'))
                break
            print ("from client", msg)
            self.info()
            if not shop:
                if (msg == "1"):
                    self.main_menu()
                elif msg == "2":
                    self.csocket.send(bytes(msg,'UTF-8'))
                elif msg == "6":
                    shop = True
                    self.shop_menu()
                elif msg == "7":
                    self.csocket.send(bytes("Your connection will be closed. Please reconnect!",'UTF-8'))
                    break
            else:
                self.csocket.send(bytes("You bought something!",'UTF-8'))
                shop = False

        print ("Client at ", clientAddress , " disconnected...")
    # Main Menu
    def main_menu(self):
        msg="""

What would you like to do?

1. Defeat the gnomes (level 10)
2. Fight a dragon (level 7)
3. Raid the cyclops (level 5)
4. Plunder the pirates (level 3)
5. Go on a journey (level 1)
6. Browse the shop
7. End journey

>"""
        self.csocket.send(bytes(msg,'UTF-8'))
    
    # Shop Menu
    def shop_menu(self):
        msg="""
1. sword (100 gold) (level 1)
2. bow (1000 gold) (level 3)
3. axe (2000 gold) (level 5)
4. missle launcher (10000 gold) (level 7)
5. tank (100000 gold) (level 10)

What would you like to buy? (press 0 to exit the shop):"""
        self.csocket.send(bytes(msg,'UTF-8'))

    def info(self):
        self.csocket.send(bytes(f"Gold: {self.gold}\r\nWeapon level: {self.weapon}\r\n",'UTF-8'))

    def welcome(self):
        msg = """Welcome to Geovillage!!!
Unfortunately, the villagers have become attacked by gnomes.

They need YOU to help take back their land!

"""
        self.csocket.send(bytes(msg,'UTF-8'))




LOCALHOST = "0.0.0.0"
PORT = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()