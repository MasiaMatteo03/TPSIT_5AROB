import socket
import threading as thr
import time


class Receiver(thr.Thread):
    def __init__(self): 
        thr.Thread.__init__(self)
        self.running = True 

    def run(self):
        while self.running:
            data, _= s.recvfrom(4096)
            print("\n"+data.decode())


def chatMode(s, nick):
    messaggio = input("inserire il messaggio: ")
    destinatario=input("inserire il destinatario: ")

    s.sendto((f"{nick}\n{destinatario}\n{messaggio}").encode(), ('localhost', 5000))


def main():
    global s 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    nick= input("inserisci il nickname ")
    s.sendto((f"nickname\n{nick}").encode(), ("localhost", 5000))  #invia il nick al server

    messaggio, indirizzo= s.recvfrom(4096) #ok
    print(messaggio.decode())

    client = Receiver()
    client.start()

    if messaggio.decode()=="ok":
        print("chat mode")
        while True:

            chatMode(s, nick)
        


main()