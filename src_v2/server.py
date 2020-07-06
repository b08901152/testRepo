import socket
from _thread import *
import sys
from gameBasic import Player, SCREENWIDTH, SCREENHEIGHT
import pickle
import pygame
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))


server = "172.20.10.3"
port = 11111

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

s.bind((server, port))
s.listen(2)
print("Waiting for a connection, Server Started")

Image = pygame.image.load(
    '../lib/image/player1.png').convert_alpha()
Image2 = pygame.image.load(
    '../lib/image/player2.png').convert_alpha()
players = [Player("harry", Image, 200, 200, 64, 64, (10, 10)),
           Player("hary", Image2, 200, 200, 64, 64, (10, 10))]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        data = pickle.loads(conn.recv(2048*1024))
        players[player] = data

        if not data:
            print("Disconnected")
            break
        else:
            if player == 1:
                reply = players[0]
            else:
                reply = players[1]

            print("Received: ", data)
            print("Sending : ", reply)

        conn.sendall(pickle.dumps(reply))

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
