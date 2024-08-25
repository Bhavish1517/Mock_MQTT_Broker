import socket
import threading

class MQTTBrokerServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.subscriptions = {}  # Stores subscriptions in a dictionary
        self.topic_messages = {}  # Stores messages published under each topic

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"MQTT Broker Server listening on {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Connection established with {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    print("Connection closed by", client_socket.getpeername())
                    self.disconnect_client(client_socket)
                    break
                self.handle_message(client_socket, data.decode())
            except OSError as e:
                if e.errno == 10038:  # Windows specific error for closed socket
                    print("Socket closed by client")
                    self.disconnect_client(client_socket)
                    break
                else:
                    raise e

    def handle_message(self, client_socket, message):
        parts = message.strip().split(" ", 1)
        command = parts[0]
        if command == "CONNECT":
            self.handle_connect(client_socket, parts[1])
        elif command == "SUBSCRIBE":
            self.handle_subscribe(client_socket, parts[1])
        elif command == "PUBLISH":
            self.handle_publish(client_socket, parts[1])
        elif command == "VIEW_SUBSCRIBED_CONTENT":
            self.handle_view_subscribed_content(client_socket)
        elif command == "DISCONNECT":
            self.disconnect_client(client_socket)
        else:
            print("Unknown command:", command)

    def handle_connect(self, client_socket, data):
        # Extract username and password from the CONNECT message
        username, password = data.split()
        
        if self.authenticate(username, password):
            # If authentication succeeds, proceed with session setup
            print(f"Client {username} connected")
        
            # Send CONNACK response to the client
            connack_msg = "CONNACK"
            client_socket.sendall(connack_msg.encode())
        
        else:
        # If authentication fails, close the connection
            print("Authentication failed")
            client_socket.close()

    def handle_subscribe(self, client_socket, data):
        topic = data.strip()
        print(f"Client subscribed to topic: {topic}")
        # Storing the subscription topic in the subscriptions dictionary
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
            # If there are stored messages for this topic, send them to the client
            if topic in self.topic_messages:
                for msg in self.topic_messages[topic]:
                    client_socket.sendall(msg.encode())
        self.subscriptions[topic].add(client_socket)

    def handle_publish(self, client_socket, data):
        # Extract topic and content from the message
        parts = data.strip().split(" ", 1)
        topic, content = parts[0], parts[1]
        print("Message received:", topic, content)
        # Store the message under the topic
        if topic not in self.topic_messages:
            self.topic_messages[topic] = []
        self.topic_messages[topic].append(content)
        
        # Publish the message to all clients subscribed to the topic or its subtopics
        for t in self.subscriptions:
            if topic.startswith(t + "/") or topic == t:
                for subscriber_socket in self.subscriptions[t]:
                    if subscriber_socket != client_socket:  # Exclude the publisher
                        subscriber_socket.sendall(data.encode())

    def handle_view_subscribed_content(self, client_socket):
        subscribed_content = {}
        for topic, subscribers in self.subscriptions.items():
            if client_socket in subscribers:
                if topic in self.topic_messages:
                    subscribed_content[topic] = self.topic_messages[topic]
        # Send the subscribed content dictionary to the client
        client_socket.sendall(str(subscribed_content).encode())


    def disconnect_client(self, client_socket):
        # Remove the client socket from subscriptions
        for topic, subscribers in self.subscriptions.items():
            if client_socket in subscribers:
                subscribers.remove(client_socket)
        client_socket.close()
        print("Client disconnected")

    def authenticate(self, username, password):
        users = {"admin": "password", "user1": "password1", "user2": "password2", "user3": "password3", "user4": "password4"}
        return username in users and users[username] == password

    def stop(self):
        for client_socket in list(self.clients.keys()):
            client_socket.close()
        self.socket.close()
        print("MQTT Broker Server stopped")

if __name__ == "__main__":
    host = "localhost"
    port = 1883
    mqtt_broker = MQTTBrokerServer(host, port)
    mqtt_broker.start()
