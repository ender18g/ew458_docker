from __future__ import print_function
import roslibpy

client = roslibpy.Ros(host='10.24.5.112', port=9012)
client.run()

client.on_ready(lambda: print('Is ROS connected?', client.is_connected))

# create subscriber
subscriber = roslibpy.Topic(client, '/juliet/ir_intensity', 'irobot_create_msgs/IrIntensityVector')

def callback(msg):
    print('\nNew message received')
    for r in msg['readings']:
        print(r['value'], end=' ')

subscriber.subscribe(callback)



try:
    while True:
        pass
        # get info on the /juliet/imu topic
except KeyboardInterrupt:
    client.terminate()