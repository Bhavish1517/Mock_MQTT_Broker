# Mock-MQTT-Broker

This project simulates an MQTT broker server and client using Python. The MQTT broker handles connections, subscriptions, and message publications between multiple clients. The client application, built with a **Tkinter-based GUI**, allows users to connect to the broker, subscribe to topics, publish messages, and view messages from subscribed topics.

Not an actual MQTT Broker like Mosquitto, HiveMQ, etc but just a simpler basic version that does not have all the functionalities of an actual MQTT Broker

## Features

- Supports multiple subscribers and publishers
- Supports nested topics
- Supports Authentication
  
### MQTT Broker Server
- Handles client connections and disconnections.
- Manages subscriptions to topics and publishes messages.
- Stores published messages for delivery to future subscribers.

### MQTT Client
- GUI-based client application using Tkinter.
- Allows users to connect to the broker with authentication.
- Provides options to subscribe to topics, publish messages, and view received messages.
- Enables users to disconnect from the broker and exit gracefully.

## Setup
- This project requires libraries like socket, threading and tkinter which are a part of Pythons's standard library and hence having Python installed is enough
- Download or Clone the repository.
- First run the server.py .
- Next on another command line run the client.py .
- You will get a basic gui to interact with and and perform different functions.
