import socket
import tkinter as tk
from tkinter import messagebox

class MQTTClient:
    def __init__(self, master, broker_host, broker_port):
        self.master = master
        self.broker_host = broker_host
        self.broker_port = broker_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((broker_host, broker_port))
            self.connected = True  
        except ConnectionRefusedError:
            print("Connection failed. Broker not available.")
            self.connected = False

        # Configure window size and position
        window_width = 400
        window_height = 500
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        # Username input
        username_frame = tk.Frame(master)
        username_frame.pack(pady=10)
        tk.Label(username_frame, text="Username:").pack(side=tk.LEFT)
        self.username_entry = tk.Entry(username_frame)
        self.username_entry.pack(side=tk.LEFT)

        # Password input
        password_frame = tk.Frame(master)
        password_frame.pack(pady=10)
        tk.Label(password_frame, text="Password:").pack(side=tk.LEFT)
        self.password_entry = tk.Entry(password_frame, show="*")
        self.password_entry.pack(side=tk.LEFT)

        # Connect button
        self.connect_button = tk.Button(master, text="Connect", command=self.connect)
        self.connect_button.pack(fill=tk.X, padx=20, pady=5)

        # Topic input for subscribe
        topic_frame = tk.Frame(master)
        topic_frame.pack(pady=10)
        tk.Label(topic_frame, text="Subscribe Topic:").pack(side=tk.LEFT)
        self.topic_entry_subscribe = tk.Entry(topic_frame)
        self.topic_entry_subscribe.pack(side=tk.LEFT)

        # Subscribe button
        self.subscribe_button = tk.Button(master, text="Subscribe", command=self.subscribe)
        self.subscribe_button.pack(fill=tk.X, padx=20, pady=5)

        # Topic input for publish
        tk.Label(master, text="Publish Topic:").pack(pady=5)
        self.topic_entry_publish = tk.Entry(master)
        self.topic_entry_publish.pack(fill=tk.X, padx=20, pady=5)

        # Content input
        tk.Label(master, text="Content:").pack()
        self.content_entry = tk.Entry(master)
        self.content_entry.pack(fill=tk.X, padx=20, pady=5)

        # Publish button
        self.publish_button = tk.Button(master, text="Publish", command=self.publish)
        self.publish_button.pack(fill=tk.X, padx=20, pady=5)

        # View subscribed content button
        self.view_button = tk.Button(master, text="View Subscribed Content", command=self.view_subscribed_content)
        self.view_button.pack(fill=tk.X, padx=20, pady=5)

        # Disconnect button
        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(fill=tk.X, padx=20, pady=5)

        # Exit button
        self.exit_button = tk.Button(master, text="Exit", command=master.quit)
        self.exit_button.pack(fill=tk.X, padx=20, pady=5)

    def connect(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        connect_msg = f"CONNECT {username} {password}"
        self.send_message(connect_msg)
        response = self.receive_message()
        if response == "CONNACK":
            messagebox.showinfo("Connect", "Connection successful")
            self.connected = True
        else:
            messagebox.showerror("Connect", "Connection failed")
            self.socket.close()
            self.connected = False

    def subscribe(self):
        topic = self.topic_entry_subscribe.get()
        subscribe_msg = f"SUBSCRIBE {topic}"
        self.send_message(subscribe_msg)
        messagebox.showinfo("Subscribe", f"Subscribed to topic: {topic}")

    def publish(self):
        topic = self.topic_entry_publish.get()
        message = self.content_entry.get()
        publish_msg = f"PUBLISH {topic} {message}"
        self.send_message(publish_msg)
        messagebox.showinfo("Publish", f"Published message: {message} to topic: {topic}")

    def view_subscribed_content(self):
        view_msg = "VIEW_SUBSCRIBED_CONTENT"
        self.send_message(view_msg)
        subscribed_content = self.receive_subscribed_message()
        subscribed_content_dict = eval(subscribed_content)
        content = ""
        for topic, messages in subscribed_content_dict.items():
            content += f"Topic: {topic}\n"
            for message in messages:
                content += f"Received: {message.strip()}\n"
        messagebox.showinfo("View Subscribed Content", content)

    def disconnect(self):
        disconnect_msg = "DISCONNECT"
        self.send_message(disconnect_msg)
        self.socket.close()
        self.connected = False
        messagebox.showinfo("Disconnect", "Disconnected")

    def send_message(self, message):
        self.socket.sendall(message.encode())

    def receive_message(self):
        return self.socket.recv(1024).decode()

    def receive_subscribed_message(self):
        message = self.socket.recv(4096).decode()
        return message.strip()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("MQTT Client")
    broker_host = "localhost"
    broker_port = 1883
    mqtt_client_gui = MQTTClient(root, broker_host, broker_port)
    root.mainloop()
