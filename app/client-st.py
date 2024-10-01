import socket

class GameClient:
    def __init__(self, server_host='localhost', server_port=12345):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.client_socket.connect((self.server_host, self.server_port))
            print(f"Connected to game server at {self.server_host}:{self.server_port}")

            # Send a connection confirmation message to the server
            self.client_socket.send("CONNECTED".encode('utf-8'))

            # Receive confirmation from server
            confirmation = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server confirmation: {confirmation}")

        except Exception as e:
            print(f"Connection failed: {e}")
            return False
        return True

    def listen_for_messages(self):
        while True:
            try:
                # Wait for messages from the server
                response = self.client_socket.recv(1024).decode('utf-8')
                if not response:
                    break
                print(f"Received from server: {response}")

            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def close(self):
        self.client_socket.close()
        print("Connection closed.")

# Example client usage
if __name__ == "__main__":
    client = GameClient()

    if client.connect():
        client.listen_for_messages()
    client.close()
