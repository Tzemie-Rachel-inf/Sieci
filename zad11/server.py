import socket

HOST = '0.0.0.0'
PORT = 2501
BUF_SIZE = 1024

clients = {}

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, PORT))
    
    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        try:
            data, addr = sock.recvfrom(BUF_SIZE)
            
            if not data:
                if addr in clients:
                    print(f"Client {clients[addr]} ({addr}) disconnected.")
                    del clients[addr]
                continue
            
            prefix = data[:1]
            payload = data[1:].decode('utf-8', errors='ignore').strip()

            if prefix == b'\x00':
                clients[addr] = payload
                print(f"User {addr} set nickname to: {payload}")
                
            elif prefix == b'\x01':
                if addr in clients:
                    nickname = clients[addr]
                    
                    formatted_msg = f"<{nickname}> {payload}\n".encode('utf-8')
                    
                    for client_addr in clients.keys():
                        sock.sendto(formatted_msg, client_addr)
                        
        except Exception as e:
            print(f"Error handling datagram: {e}")

if __name__ == "__main__":
    main()
