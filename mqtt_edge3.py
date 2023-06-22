import paho.mqtt.client as mqtt
import json
import logging
logging.basicConfig(level = logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
from pymongo.errors import PyMongoError
from pymongo import MongoClient
from pymongo.errors import PyMongoError
import requests

client = MongoClient('mongodb://root:root@192.168.80.242:14')
db = client['PTIN']
dron = db['Drones']
orders = db['Orders']


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
    #Aqui podemos poner los ifs para definir un tema determinado
    
    #----------------------------------------------------------------------------------------
    if msg.topic == "PTIN2023/SITGES/DRON/UPDATELOCATION":
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron','location_act','status','status_num','battery','autonomy']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                print("---------------------------------------")
                update_fields = {
                    'location_act': payload['location_act'],
                    'status': payload['status'],
                    'battery': payload['battery'],
                    'autonomy': payload['autonomy'],
                    'status_num' : payload['status_num']
                }
                # Filtra por id_car y actualiza los demás campos
                try:
                    result = dron.update_one(
                        {'id_dron': payload['id_dron']},  # Filtra por el valor de id_car
                        {'$set': update_fields}  # Define los campos y valores a actualizar
                    )
                    if result.modified_count > 0:
                        print("Documento actualizado correctamente")
                    else:
                        print(str(payload['id_dron']))
                        print("El documento no se actualizó. Puede que no se encontrara el id_dron especificado.UPDATELOCATION")
                        
                except PyMongoError as e:
                    print("Ocurrió un error al actualizar el documento:", str(e))
                    
            else: 
                print("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | UPDATELOCATION")
#-----------------------------------------------------------------------------------------    
    if msg.topic == "PTIN2023/SITGES/DRON/UPDATESTATUS":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'status','status_num']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                print("---------------------------------------")
                print('Estado: ', payload['status_num'])
                if payload['status_num'] == 3 or payload['status_num']==4 or payload['status_num']==9 or payload['status_num']==10:
                    print("entro")
                    if payload['status_num']==3:
                        state='drone_sent'
                        state_num=4
                    elif payload['status_num']==4:
                        state='delivered_awaiting'
                        state_num=5
                    elif payload['status_num']==9:
                        state='delivered'
                        state_num=9
                    elif payload['status_num']==10:
                        state='not delivered'
                        state_num=10
                    
                    print("status: " , payload['status_num'])

                    id_pack=dron.find_one(
                        {'id_dron': payload['id_dron']}, 
                        {'id_pack': 1}
                    )['id_pack']
                    
                    print("idpacl= "+str(id_pack))
                    update_fields2 = {
                        'state': state,
                        'state_num' : state_num
                    }
                    Response=orders.update_one(
                    {'order_identifier': id_pack},  # Filtra por el valor de id_pack
                    {'$set': update_fields2}  # Define los campos y valores a actualizar

                    )                
                
                
                
                
                
                
                
                update_fields = {
                    'status': payload['status'],
                    'status_num' : payload['status_num']
                }
                # Filtra por id_car y actualiza los demás campos
                try:
                    result = dron.update_one(
                        {'id_dron': payload['id_dron']},  # Filtra por el valor de id_car
                        {'$set': update_fields}  # Define los campos y valores a actualizar
                    )
                    if result.modified_count > 0:
                        print("Documento actualizado correctamente")
                    else:
                        print(str(payload['id_dron']))

                        print("El documento no se actualizó. Puede que no se encontrara el id_dron especificado.updatestatus")
                        
                except PyMongoError as e:
                    print("Ocurrió un error al actualizar el documento:", str(e))
                    
            else: 
                print("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | UPDATESTATUS")          
#-----------------------------------------------------------------------------------------    



    if msg.topic == "PTIN2023/SITGES/A2/FRAN/JOA":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'status']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                
                print("Enviado a la BD id_dron " + str(payload["id_dron"]) +" y status" + str(payload["status"]))
                print("---------------------------------------")
            
            else:
                print("PTIN2023/A2/FRAN")        
        else:
            print("Recibido el texto plano siguiente: "+msg.payload.decode('utf-8'))

            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.80.241", 1883 , 60)
client.loop_forever()