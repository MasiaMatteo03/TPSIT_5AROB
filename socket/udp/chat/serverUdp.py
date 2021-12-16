import socket as sck

client = {}

OK = "ok"

def main():
    s = sck.socket(sck.AF_INET, sck.SOCK_DGRAM)
    s.bind(('0.0.0.0', 5000))


    while True:
        messaggio, indirizzo = s.recvfrom(4096)
        messaggio = messaggio.decode()
        #print(messaggio)
        messaggio = messaggio.split('\n')

        if messaggio[0].lower() == "nickname":    #messaggio di hello
            print(f"nuova iscrizione {messaggio[1]}")
            client[messaggio[1]] = indirizzo
            s.sendto(OK.encode(), client[messaggio[1]])
        else:       #messaggio normale

            for k in client.keys():
                if k == messaggio[1]:
                    print(f"{messaggio[0]} manda a {messaggio[1]} : {messaggio[2]}")
                    s.sendto(messaggio[2].encode(),client[k])
        
       

    s.close()

main()