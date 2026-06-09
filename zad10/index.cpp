#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>

using namespace std;

char buffer[2048];

int main(int argc, char* argv[]) {
    if (getuid() == 0) {
        cerr << "Error: Uruchamianie z konta root jest zablokowane.\n";
        return 1;
    }

    int port = 80;
    if (argc > 1) {
        port = strtol(argv[1], NULL, 10);
    }

    int sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP);
    if (sock < 0) {
        perror("socket error");
        return 1;
    }

    int value = 1;
    if (setsockopt(sock, SOL_SOCKET, SO_REUSEADDR, (const char*)&value, sizeof(value)) < 0) {
        perror("setsockopt error");
        close(sock);
        return 1;
    }

    struct sockaddr_in addr;
    memset((char*)&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(port);

    if (bind(sock, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        perror("bind error");
        close(sock);
        return 1;
    }

    if (listen(sock, 80) < 0) {
        perror("listen error");
        close(sock);
        return 1;
    }

    const char* http_header = "HTTP/1.0 200 OK\r\n"
                              "Content-Type: text/plain; charset=UTF-8\r\n"
                              "Connection: close\r\n";

    while (true) {
        struct sockaddr_in client_addr;
        socklen_t length = sizeof(client_addr);
        
        int handle = accept(sock, (struct sockaddr*)&client_addr, &length);
        if (handle < 0) {
            perror("accept error");
            close(sock);
            return 1;
        }

        if (recv(handle, buffer, sizeof(buffer) - 1, 0) < 0) {
            perror("recv error");
            close(handle);
            continue; 
        }

        ifstream file("/proc/uptime");
        string uptime = "";
        if (file.good()) {
            file >> uptime;
        } else {
            perror("file read error");
        }
        file.close();

        string headers = string(http_header) + 
                         "Content-Length: " + to_string(uptime.length()) + 
                         "\r\n\r\n";

        if (send(handle, headers.c_str(), headers.length(), 0) < 0) {
            perror("send headers error");
            close(handle);
            continue;
        }

        if (send(handle, uptime.c_str(), uptime.length(), 0) < 0) {
            perror("send content error");
            close(handle);
            continue;
        }

        if (shutdown(handle, SHUT_WR) < 0) {
            perror("shutdown error");
        }

        if (close(handle) < 0) {
            perror("close handle error");
        }
    }
    
    if (close(sock) < 0) {
        perror("close socket error");
    }
    
    return 0;
}
