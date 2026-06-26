import paho.mqtt.client as mqtt
# Define the callback function when a message is received
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    print(f"Received message: {payload} on topic: {message.topic}")
# Define the callback function when successfully connected
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Successfully connected to the MQTT broker!")
        # Subscribe to the target topic
        client.subscribe("ashraf/power")
        print("Subscribed to topic: ashraf/power")
    else:
        print(f"Connection failed with code {rc}")
def main():
    # Create an MQTT client instance
    # Note: Callback API version 1 is used here for maximum compatibility
    client = mqtt.Client()
    # Assign the callback functions
    client.on_connect = on_connect
    client.on_message = on_message
    # Connect to the local broker running on the Pi
    broker_address = "localhost"
    port = 1883
    print(f"Connecting to broker at {broker_address}...")
    client.connect(broker_address, port, 60)
    # Start the loop to process network traffic and dispatch callbacks
    # This blocks the script so it stays alive to listen for messages
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDisconnecting from broker...")
        client.disconnect()
        print("Exited successfully.")
if __name__ == "__main__":
    main()
