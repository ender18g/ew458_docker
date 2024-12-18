from sense_hat import SenseHat
import time
import socket
import os

sense = SenseHat()

def get_ip_address():
    """
    Retrieve the IP address of the Raspberry Pi.
    """
    try:
        # get the wlan0 IP address
        #         inet 192.168.11.42  netmask 255.255.255.0  broadcast 192.168.11.255
        ip_address = os.popen("ifconfig wlan0 | grep 'inet ' | sed -E 's/.*inet ([0-9.]+).*/\\1/'").read().strip()
    except:

        ip_address = "No IP"
    return ip_address

def display_ip_address():
    """
    Scroll the IP address across the Sense HAT LED matrix.
    """
    ip_address = get_ip_address()
    print(f"IP Address: {ip_address}")  # Print to the console for verification
    sense.show_message(f"IP: {ip_address}", scroll_speed=0.05, text_colour=[150, 0, 150])

if __name__ == "__main__":
    for i in range(3):
        display_ip_address()
