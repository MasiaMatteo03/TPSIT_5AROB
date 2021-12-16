import socket
import threading as thr
import time

registered = False
nickname = ""

class Receiver(thr.Thread):
    def __init__(self, s): 
        thr.Thread.__init__(self)
        self.running = True 
        self.s = s

    def stop_run(self):
        self.running = False

    def run(self):
        global registered

        while self.running:
            data = self.s.recv(4096).decode()

            if data == "OK":
                registered = True
                print(f"\nConnessione avvenuta, registrato. Entrando nella chat mode...")
            
            else:
                print(f"\n{data}")

def main():
    global registered
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('192.168.0.100', 5000))

    client = Receiver(s)
    client.start()

    while True:
        time.sleep(0.2)

        if not registered:
            nickname = input("Inserisci un nickname >>>")

            mex = "Nickname:" + nickname
            registered = True

        else:
            destinatario = input("Inserisci il destinatario >>>")

            text = input("Inserisci il messaggio >>>")
            mex = nickname + ":" + destinatario + ":" + text

        s.sendall(mex.encode())

        if 'exit' in mex.split(":"):
            client.stop_run()
            print("Disconnessione...")
            break

    client.join()
    s.close()

if __name__ == "__main__":
    main()