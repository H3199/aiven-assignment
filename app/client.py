import socket
import json

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

    def send_request(self, action):
        try:
            # Send a request to the server
            request = json.dumps(action)
            self.client_socket.send(request.encode('utf-8'))

            # Receive the response from the server
            response = self.client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
        except Exception as e:
            print(f"Error sending request: {e}")

    def close(self):
        self.client_socket.close()
        print("Connection closed.")

# Example client usage
if __name__ == "__main__":
    client = GameClient()

    if client.connect():
        # Example action: Move an item
    #    action = {
    #        'action': 'move',
    #       'item_id': 1,
    #       'from_container_id': 1,
    #        'to_container_id': 2
    #    }
       action = {'action': 'get_containers'}
       client.send_request(action)

        # Close the connection after the request
    client.close()
