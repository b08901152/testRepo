import socket
from _thread import *
import sys

server = "172.20.10.4"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

text = ["",""]
def threaded_client(conn,currentPlayer):
    conn.send(str.encode("Connected"))
    reply = ""
    while True:
       
        data = conn.recv(2048*4096)
        reply = data.decode("utf-8")
        text[currentPlayer] = reply
            
        if currentPlayer == 1:
            reply = text[1]
        if currentPlayer == 2:
            reply = text[0]
        print("Received: ", data)
        print("Sending : ", reply)
        conn.sendall(str.encode(reply))
        conn.close()

    print("Lost connection")


currentPlayer = 0

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer+=1
    print(currentPlayer)
