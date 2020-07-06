import socket
from _thread import *
from player import Player
import pickle
import pygame

server = "140.112.241.16"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

Image = pygame.image.load(
    '../lib/image/player1.png')  # player1要用的圖
player1 = Player("harry", Image, 200, 200, 64, 64, (10, 10))

Image2 = pygame.image.load(
    '../lib/image/player2.png')  # player2要用的圖
player2 = Player("hary", Image2, 200, 200, 64, 64, (10, 10))
players = [player1,player2]


def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(2048*100))
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
        except:
            break

    print("Lost connection")
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
