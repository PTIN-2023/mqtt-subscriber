import paho.mqtt.client as mqtt
import logging
import os

from mqtt_cloud import on_connect as on_connect_cloud
from mqtt_cloud import on_message as on_message_cloud
from mqtt_edge import on_connect as on_connect_edge
from mqtt_edge import on_message as on_message_edge

mqtt_server_address = os.environ.get('MQTT_SERVER_ADDRESS')
mqtt_server_port = os.environ.get('MQTT_SERVER_PORT')
is_local = os.environ.get('IS_LOCAL')

def start_mqtt_subscriber():
    # Create an MQTT client
    client = mqtt.Client()

    # Set up callback functions
    if is_local == 0:
        client.on_connect = on_connect_cloud
        client.on_message = on_message_cloud
    else:
        client.on_connect = on_connect_edge
        client.on_message = on_message_edge

    # Connect to the MQTT broker running in the mosquitto container
    client.connect("mosquitto", 1883, 60)

    # Start the MQTT subscriber loop
    client.loop_forever()

if __name__ == "__main__":
    # Configure the logging settings
    logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
    # logging.info("This is an info log message")# Log a message
    # logging.error("This is an error log message")# Log an error
    # logging.warning("This is a warning log message")# Log a warning
    start_mqtt_subscriber()