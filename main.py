#!/usr/bin/env python3

import socket
import threading
import random
import os

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def repl(self, msg):
        self.csocket.send(bytes("\r\n\r\n"+msg,'UTF-8'))
    # Main Function
    def run(self):
        print ("Connection from : ", clientAddress)
        msg = ''
        # Main vars.. required for each con.
        self.alive = True
        self.shop = False
        self.gold = 100
        self.weapon = 0
        self.welcome()
        self.info()
        self.main_menu()

        # Main loop
        while self.alive:
            data = self.csocket.recv(2048)
            msg = data.decode("UTF-8").rstrip()
            if (not data):
                self.repl("Your connection will be closed. Please reconnect!")
                break
            #print ("from client", msg)
            if not self.shop:
                if (msg == "1"):
                    self.fight(10)
                elif msg == "2":
                    self.fight(7)
                elif msg == "3":
                    self.fight(5)
                elif msg == "4":
                    self.fight(3)
                elif msg == "5":
                    self.fight(1)
                elif msg == "6":
                    self.shop = True
                    self.info()
                    self.shop_menu()
                elif msg == "7":
                    break
            else:
                if (msg == "1"):
                    if self.gold >= 100:
                        self.gold = self.gold-100
                        self.weapon = 1
                        self.repl("You bought a nice looking sword!")
                    else:
                        self.repl("You can not afford to buy this!")
                elif (msg == "2"):
                    if self.gold >= 1000:
                        self.gold = self.gold-1000
                        self.weapon = 3
                        self.repl("You bought a awsome bow!")
                    else:
                        self.repl("You can not afford to buy this!")
                elif (msg == "3"):
                    if self.gold >= 2000:
                        self.gold = self.gold-2000
                        self.weapon = 5
                        self.repl("You bought a really sharp axe!")
                    else:
                        self.repl("You can not afford to buy this!")
                elif (msg == "4"):
                    if self.gold >= 10000:
                        self.gold = self.gold-10000
                        self.weapon = 7
                        self.repl("You bought a old rusty missle launcher!")
                    else:
                        self.repl("You can not afford to buy this!")
                elif (msg == "5"):
                    if self.gold >= 100000:
                        self.gold = self.gold-100000
                        self.weapon = 10
                        self.repl("You bought a big tank!")
                    else:
                        self.repl("You can not afford to buy this!")
                self.shop = False
                self.info()
                self.main_menu()
        
        self.repl("Your connection will be closed. Please reconnect!")
        print("Client at ", clientAddress , " disconnected...")

    #Fight something
    def fight(self, level):
        if self.weapon < level:
            self.repl(f"Are you sure? With your weapon level of {self.weapon} you have a 0\% success rate. (y/n): ")
            data = self.csocket.recv(2048)
            msg = data.decode("UTF-8").rstrip()
            if(msg == "y"):
                quote_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), f"{level}_die.txt")
                f = open(quote_file, 'r')
                txt = f.read()
                lines = txt.split('\n.\n')
                f.close()
                self.repl(random.choice(lines))
                self.alive = False
        else:
            if level == 10:
                self.flag()
            else:
                reward = random.randint(1, 10) * level
                self.gold = self.gold + reward
                self.repl(f"Congrats you have returned from your journey with {reward} gold")
            self.info()
            self.main_menu()

    # Main Menu
    def main_menu(self):
        msg="""What would you like to do?

1. Defeat the gnomes (level 10)
2. Fight a dragon (level 7)
3. Raid the cyclops (level 5)
4. Plunder the pirates (level 3)
5. Go on a journey (level 1)
6. Browse the shop
7. End journey

>"""
        self.repl(msg)
    
    # Shop Menu
    def shop_menu(self):
        msg="""1. sword (100 gold) (level 1)
2. bow (1000 gold) (level 3)
3. axe (2000 gold) (level 5)
4. missle launcher (10000 gold) (level 7)
5. tank (100000 gold) (level 10)

What would you like to buy? (press 0 to exit the shop):"""
        self.repl(msg)

    def info(self):
        self.repl(f"Gold: {self.gold}\r\nWeapon level: {self.weapon}\r\n")

    def welcome(self):
        msg = """Welcome to Geovillage!!!
Unfortunately, the villagers have become attacked by gnomes.

They need YOU to help take back their land!

"""
        self.repl(msg)
    
    # Finish
    def flag(self):
        quote_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "flag.txt")
        f = open(quote_file, 'r')
        txt = f.read()
        self.repl(txt)




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