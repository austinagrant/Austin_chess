
import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 65432))
    server_socket.listen()

    print("Server listening on port 65432...")
    conn, addr = server_socket.accept()
    print(f"Connected by {addr}")

    try:
        # Receive data from client
        data = conn.recv(1024)
        if not data:
            print("No data received.")
        else:
            print(f"Received {len(data)} bytes: {data.decode()}")

            # Send response to client
            response = "Hello from Python"
            conn.sendall(response.encode())
            print(f"Sent {len(response)} bytes: {response}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    start_server()



