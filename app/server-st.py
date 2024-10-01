import socket
import json
from confluent_kafka import Consumer, KafkaError

class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(1)  # Only accept one client
        print(f"Server started at {self.host}:{self.port}")

        # TODO: hardcoded values
        # These should be from github secrets,
        # but we'd need to have CI/CD pipeline for the game server.
        # We could build a docker image for the server and run that somewhere,
        # but this is statarting to become a swamp of scope creep.
        self.kafka_consumer = Consumer({
            'bootstrap.servers': 'assignment-kafka-eerohaavisto-49ce.d.aivencloud.com:20484',
            'security.protocol': 'SSL',
            'ssl.ca.location': '/home/eero/aiven/aiven-assignment/infra/kafka/ca.pem',
            'ssl.certificate.location': '/home/eero/aiven/aiven-assignment/infra/kafka/service.cert',
            'ssl.key.location': '/home/eero/aiven/aiven-assignment/infra/kafka/service.key',
            'group.id': 'avnadmin',
            'auto.offset.reset': 'earliest'
        })

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")

        try:
            # Wait for a connection confirmation from the client
            confirmation = client_socket.recv(1024).decode('utf-8')
            if confirmation == "CONNECTED":
                print(f"Client {address} confirmed connection.")
                client_socket.send("Connection confirmed.".encode('utf-8'))

                # Start consuming messages
                self.consume_messages(client_socket)

            else:
                print(f"Unexpected confirmation message from {address}: {confirmation}")
                client_socket.send("Unexpected confirmation.".encode('utf-8'))
                client_socket.close()
                return

        except Exception as e:
            print(f"Error handling client confirmation: {e}")
            client_socket.close()
            return

    def consume_messages(self, client_socket):
        topic = 'gamedata.public.items'  # Replace with your actual topic
        self.kafka_consumer.subscribe([topic])

        while True:
            try:
                msg = self.kafka_consumer.poll(1.0)  # Wait up to 1 second for a message
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event
                        continue
                    else:
                        print(f"Error while consuming: {msg.error()}")
                        continue

                # Send the consumed message to the connected client
                message_value = msg.value().decode('utf-8')
                client_socket.send(f"KAFKA: {message_value}".encode('utf-8'))

            except Exception as e:
                print(f"Error in Kafka consumer: {e}")
                break

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            self.handle_client(client_socket, client_address)

    def close(self):
        self.kafka_consumer.close()
        self.server_socket.close()


# Example server usage
if __name__ == "__main__":
    server = GameServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("Server shutting down.")
        server.close()
