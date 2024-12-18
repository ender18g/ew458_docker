#import rospy
import roslibpy

def on_message_received(message):
    print(f"Received message: {message}")

def list_topics(ros_client):
    service = roslibpy.Service(ros_client, '/rosapi/topics', 'rosapi/Topics')
    request = roslibpy.ServiceRequest({})

    def callback(result):
        print("Available topics:")
        for topic in result['topics']:
            print(f"- {topic}")

    service.call(request, callback)

def main():
    ros_client = roslibpy.Ros(host='127.0.0.1', port=9091)
    ros_client.run()

    if ros_client.is_connected:
        print("Connected to ROS bridge.")

        # List all message topics
        list_topics(ros_client)

        # Subscribe to /chatter topic
        chatter_listener = roslibpy.Topic(ros_client, '/chatter', 'std_msgs/String')
        chatter_listener.subscribe(on_message_received)

        try:
            # Keep the script running to listen to messages
            print("Listening to /chatter topic. Press Ctrl+C to exit.")
            while True:
                pass
        except KeyboardInterrupt:
            print("Exiting...")
        finally:
            chatter_listener.unsubscribe()
            ros_client.terminate()

if __name__ == "__main__":
    main()
