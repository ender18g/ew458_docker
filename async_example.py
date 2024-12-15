import roslibpy
import time

# Define the main function to make the script modular
def main():
    """
    A simple example of using roslibpy to connect to a ROS bridge, subscribe to a topic,
    and publish messages to another topic.
    """

    # Step 1: Connect to the ROS bridge
    # Replace '172.0.0.1' with the actual IP address of your ROS bridge if needed
    client = roslibpy.Ros(host='127.0.0.1', port=9091)

    print('Attempting to connect to ROS bridge...')
    client.run()
    print('Connected to ROS bridge!')

    # Step 2: Subscribe to the /chatter topic
    def chatter_callback(message):
        """
        Callback function that gets executed when a new message is published on the /chatter topic.
        """
        print(f"Received message on /chatter: {message['data']}")

    chatter_listener = roslibpy.Topic(client, '/chatter', 'std_msgs/String')
    chatter_listener.subscribe(chatter_callback)

    # Step 3: Publish to the /chatter2 topic every 500 ms
    global counter
    counter = 0  # Initialize a global counter

    def publish_to_chatter2():
        """
        Function to publish messages to the /chatter2 topic every 500 ms.
        """
        chatter2_publisher = roslibpy.Topic(client, '/chatter2', 'std_msgs/String')
        while client.is_connected:
            global counter
            counter += 1
            message = roslibpy.Message({'data': f'Counter: {counter}'})
            chatter2_publisher.publish(message)
            print(f"Published message to /chatter2: {message['data']}")
            time.sleep(0.5)

    print("Listening to /chatter and publishing to /chatter2...")

    # Run the publisher in a separate loop
    try:
        publish_to_chatter2()
    except KeyboardInterrupt:
        print("Disconnecting...")

    # Cleanup: Unsubscribe and close connections
    chatter_listener.unsubscribe()
    client.terminate()
    print("Disconnected from ROS bridge.")

# Run the main function
if __name__ == '__main__':
    main()
