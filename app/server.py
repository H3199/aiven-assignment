import uuid
import psycopg2
from psycopg2 import sql
import json
import socket
import threading


class GameServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server started at {self.host}:{self.port}")

        # Database connection setup
        # TODO: hardcoded values
        # admin password in github, nice.
        print("Connecting to database...")
        self.db_conn = psycopg2.connect(
            dbname="defaultdb", user="avnadmin", password="AVNS_XVoel8gEFJDDHxXrMmH", host="postgresql-eerohaavisto-49ce.d.aivencloud.com", port=20482
        )
        self.db_conn.autocommit = False
        self.db_cursor = self.db_conn.cursor()
        print("Database connection established.")

    def handle_client(self, client_socket, address):
        print(f"New connection from {address}")

        # Wait for a connection confirmation from the client
        try:
            confirmation = client_socket.recv(1024).decode('utf-8')
            if confirmation == "CONNECTED":
                print(f"Client {address} confirmed connection.")
                client_socket.send("Connection confirmed.".encode('utf-8'))
            else:
                print(f"Unexpected confirmation message from {address}: {confirmation}")
                client_socket.send("Unexpected confirmation.".encode('utf-8'))
                client_socket.close()
                return

        except Exception as e:
            print(f"Error handling client confirmation: {e}")
            client_socket.close()
            return

        while True:
            try:
                # Receive client request
                request = client_socket.recv(1024).decode('utf-8')
                if not request:
                    break

                # Process client request
                response = self.process_request(request)
                client_socket.send(response.encode('utf-8'))

            except Exception as e:
                print(f"Error handling client: {e}")
                break

        client_socket.close()
        print(f"Connection closed for {address}")

    def process_request(self, request):
        try:
            action = json.loads(request)
            if action['action'] == 'move':
                item_id = action['item_id']
                from_container_id = action['from_container_id']
                to_container_id = action['to_container_id']
                self.move_item(item_id, from_container_id, to_container_id)
                return f"Item {item_id} moved from {from_container_id} to {to_container_id}"

            elif action['action'] == 'get_containers':
                containers = self.get_containers()
                return json.dumps({'containers': containers})

            elif action['action'] == 'get_container_contents':
                container_id = action['container_id']
                contents = self.get_container_contents(container_id)
                return json.dumps({'container_id': container_id, 'contents': contents})

            else:
                return "Unknown action"

        except Exception as e:
            print(f"Error processing request: {e}")
            return "Error processing request"

    def get_containers(self):
        # Retrieve all containers from the database.
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT container_id, container_name FROM containers;")
        containers = cursor.fetchall()
        cursor.close()
        return containers

    def get_container_contents(self, container_id):
        # Retrieve all items in the specified container
        cursor =self.db_conn.cursor()
        query = """
            SELECT i.item_id, i.item_name
            FROM container_items ci
            JOIN items i ON ci.item_id = i.item_id
            WHERE ci.container_id = %s;
        """
        cursor.execute(query, (container_id,))
        contents = cursor.fetchall()
        cursor.close()
        return contents

    def move_item(self, item_id, from_container_id, to_container_id):
        try:
            self.db_cursor.execute(
                "DELETE FROM container_items WHERE container_id = %s AND item_id = %s",
                (from_container_id, item_id)
            )
            self.db_cursor.execute(
                "INSERT INTO container_items (container_id, item_id) VALUES (%s, %s)",
                (to_container_id, item_id)
            )
            self.db_conn.commit()
        except Exception as e:
            self.db_conn.rollback()
            print(f"Error moving item: {e}")

    def start(self):
        while True:
            client_socket, client_address = self.server_socket.accept()
            client_handler = threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address)
            )
            client_handler.start()

    def close(self):
        self.db_cursor.close()
        self.db_conn.close()
        self.server_socket.close()

class Character:
    def __init__(self, name, character_type='Player'):
        self.id = uuid.uuid4()
        self.name = name
        self.character_type = character_type  # 'Player' or 'NPC'
        self.inventory = Container(name=f"{name}'s Inventory", rows=6, columns=8)

    def pick_up_item(self, item, container):
        # Picks up an item from the given container and adds it to the character's inventory
        if container.remove_item(item):
            self.inventory.add_item(item)
            print(f"{self.name} picked up {item.name} from {container.name}.")
        else:
            print(f"{item.name} not found in {container.name}.")

    def drop_item(self, item, container):
        # Drops an item from the inventory into another container
        if self.inventory.remove_item(item):
            container.add_item(item)
            print(f"{self.name} dropped {item.name} into {container.name}.")
        else:
            print(f"{self.name} doesn't have {item.name}.")

    def view_inventory(self):
        return self.inventory.view_items()


class Item:
    def __init__(self, name, item_type, stackable=False, quantity=1):
        self.id = uuid.uuid4()
        self.name = name
        self.item_type = item_type  # Example: 'Weapon', 'Potion'
        self.stackable = stackable
        self.quantity = quantity if stackable else 1


class Container:
    def __init__(self, name, rows, columns):
        self.id = uuid.uuid4()
        self.name = name
        self.rows = rows
        self.columns = columns
        self.items = []  # Grid-based or simple list-based for now

    def add_item(self, item):
        self.items.append(item)
        print(f"{item.name} added to {self.name}.")

    def remove_item(self, item):
        for i, inv_item in enumerate(self.items):
            if inv_item.id == item.id:
                del self.items[i]
                print(f"{item.name} removed from {self.name}.")
                return True
        return False

    def view_items(self):
        return [item.name for item in self.items]

# TODO: no hardcoded values
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname="defaultdb", user="avnadmin", password="AVNS_XVoel8gEFJDDHxXrMmH", host="postgresql-eerohaavisto-49ce.d.aivencloud.com"
        )
        self.conn.autocommit = False

    def move_item_transaction(self, item_id, from_container_id, to_container_id):
        with self.conn:
            with self.conn.cursor() as cursor:
                try:
                    # Remove the item from the source container
                    cursor.execute("""
                        DELETE FROM container_items
                        WHERE container_id = %s AND item_id = %s
                    """, (from_container_id, item_id))

                    # Add the item to the destination container
                    cursor.execute("""
                        INSERT INTO container_items (container_id, item_id, quantity, grid_x, grid_y)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (to_container_id, item_id, 1, 0, 0))

                    print(f"Item {item_id} moved successfully.")

                except Exception as e:
                    self.conn.rollback()
                    print(f"Error during transaction: {e}")
                    raise  # Rethrow after rollback

                else:
                    # Commit is automatic with the context manager unless there is an exception
                    print("Transaction successful")

if __name__ == "__main__":
    server = GameServer()
    server.start()
