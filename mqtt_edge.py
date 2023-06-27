import paho.mqtt.client as mqtt
import json
import logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from pymongo.errors import PyMongoError
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import requests
import os

mongo_host = os.environ.get('DB_HOST')
mongo_port = os.environ.get('DB_PORT')
mqtt_topic_city = os.environ.get('MQTT_TOPIC_CITY')
api_url = os.environ.get('API')

def is_json(data):
    try:
        json.loads(data)
        return True
    except json.decoder.JSONDecodeError:
        return False

def on_connect(client, userdata, flags, rc):
    print("Edge conectado con codigo "+str(rc))
    client.subscribe("PTIN2023/#")

def on_message(client, userdata, msg):
    
    print(msg.topic)
    
    #----------------------------------------------------------------------------------------
    if msg.topic == "PTIN2023/"+mqtt_topic_city+"/DRON/UPDATELOCATION":
        if(is_json(msg.payload.decode('utf-8'))):
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'location_act', 'status', 'status_num', 'battery', 'autonomy']
            if all(key in payload for key in needed_keys):                
                logging.info("update llega aqui siu")
                url = api_url + "/api/update_location"
                response =  requests.post(url, json = payload)
            else: 
                logging.info("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | UPDATELOCATION")
                
#-----------------------------------------------------------------------------------------    
    if msg.topic == "PTIN2023/"+mqtt_topic_city+"/DRON/UPDATESTATUS":#Hay que poner un tema en común, sinó se petará todo
       
        if(is_json(msg.payload.decode('utf-8'))):
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'status', 'status_num']
            if all(key in payload for key in needed_keys):
                logging.info("status llega aqui siu")
                url = api_url + "/api/update_status"
                response =  requests.post(url, json = payload)              
                    