import roslibpy
import sys
import termios
import tty
import threading

# Constants for velocities
LINEAR_SPEED = 0.2   # Adjust linear speed (m/s)
ANGULAR_SPEED = 0.5  # Adjust angular speed (rad/s)

# Robot Connection Settings
ROBOT_IP = '192.168.7.57'
PORT = 9012
topic_name = '/juliet/cmd_vel'

# Function to capture single keyboard input
def get_key():
    tty.setraw(sys.stdin.fileno())
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, termios.tcgetattr(sys.stdin))
    return key

# Twist command publisher class
class TeleopTwistPublisher:
    def __init__(self, client, topic):
        self.client = client
        self.publisher = roslibpy.Topic(client, topic, 'geometry_msgs/Twist')
        self.linear = 0.0
        self.angular = 0.0
        self.running = True

    def send_twist(self):
        twist = {
            'linear': {'x': self.linear, 'y': 0.0, 'z': 0.0},
            'angular': {'x': 0.0, 'y': 0.0, 'z': self.angular}
        }
        self.publisher.publish(roslibpy.Message(twist))

    def stop(self):
        self.linear = 0.0
        self.angular = 0.0
        self.send_twist()

    def control_loop(self):
        print("\nUse arrow keys to control the robot:")
        print("UP: Forward, DOWN: Backward, LEFT: Turn Left, RIGHT: Turn Right")
        print("Press 'q' to quit.\n")
        while self.running:
            try:
                key = get_key()
                if key == '\x1b':  # Arrow key prefix
                    if get_key() == '[':
                        arrow = get_key()
                        if arrow == 'A':  # UP
                            self.linear = LINEAR_SPEED
                            self.angular = 0.0
                        elif arrow == 'B':  # DOWN
                            self.linear = -LINEAR_SPEED
                            self.angular = 0.0
                        elif arrow == 'C':  # RIGHT
                            self.linear = 0.0
                            self.angular = -ANGULAR_SPEED
                        elif arrow == 'D':  # LEFT
                            self.linear = 0.0
                            self.angular = ANGULAR_SPEED
                elif key == 'q':
                    print("Exiting...\n")
                    self.running = False
                    break
                else:
                    self.linear = 0.0
                    self.angular = 0.0
                self.send_twist()
            except KeyboardInterrupt:
                self.running = False
                break
        self.stop()

# Main function to connect to ROS and control the robot
def main():
    print("Connecting to robot at {}:{}...".format(ROBOT_IP, PORT))
    client = roslibpy.Ros(host=ROBOT_IP, port=PORT)

    try:
        client.run()
        if client.is_connected:
            print("Connected successfully to ROS. Starting teleop control.")
            publisher = TeleopTwistPublisher(client, topic_name)
            publisher.control_loop()
        else:
            print("Failed to connect to ROS.")
    except Exception as e:
        print("Error:", e)
    finally:
        if client.is_connected:
            client.terminate()
        print("Connection closed.")

if __name__ == '__main__':
    main()