import socket
import select
import sys

SERVER_IP = '127.0.0.1' 
SERVER_PORT = 2501
BUF_SIZE = 1024

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sock.setblocking(False)
    
    server_addr = (SERVER_IP, SERVER_PORT)
    print("Connected. Type '/yournick' to set nickname, then type to send messages.")

    try:
        while True:
            readable, _, _ = select.select([sock, sys.stdin], [], [])
            
            for s in readable:
                if s == sys.stdin:
                    msg = sys.stdin.readline()
                    
                    if not msg:
                        sock.sendto(b"", server_addr)
                        return
                    
                    msg = msg.strip()
                    if not msg:
                        continue
                        
                    if msg.startswith('/'):
                        data = b'\x00' + msg[1:].encode('utf-8')
                    else:
                        data = b'\x01' + msg.encode('utf-8')
                        
                    sock.sendto(data, server_addr)
                    
                elif s == sock:
                    try:
                        data, _ = sock.recvfrom(BUF_SIZE)
                        if data:
                            print(data.decode('utf-8', errors='ignore'), end='')
                    except BlockingIOError:
                        pass
                        
    except KeyboardInterrupt:
        sock.sendto(b"", server_addr)
    finally:
        sock.close()

if __name__ == "__main__":
    main()
