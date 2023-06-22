import paho.mqtt.client as mqtt
import json
import requests
import logging

def is_json(data):
    try:
        json.loads(data)
        return True
    except json.decoder.JSONDecodeError:
        return False

def on_connect(client, userdata, flags, rc):
    print("Cloud conectado con codigo " + str(rc))
    client.subscribe("PTIN2023/#")

# Aqui podemos poner los ifs para definir un tema determinado
def on_message(client, userdata, msg):
    
    if msg.topic == "PTIN2023/A2/INCLOUD":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['KEY1', 'KEY2', 'KEY3']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                print("Enviado al CLOUD [KEY1],[KEY2],[KEY3]")
                print("Enviado a la BD KEY1,KEY2,KEY3("+str(payload["KEY1"]) + ","+str(payload["KEY2"]) +","+str(payload["KEY2"]+")"))
                print("---------------------------------------")
            
            else:
                print("ERROR FORMATO!-->PTIN2023/A2/TOCLOUD")        
        else:
            print("Recibido el texto plano siguiente: "+msg.payload.decode('utf-8'))

#----------------------------------------------------------------------------------------
    if msg.topic == "PTIN2023/A2/USERINCLOUD":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['email', 'password']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                # Hacer una solicitud POST a la ruta /api/login con los datos recibidos por MQTT
                #url = 'http://localhost:5000/api/login'  # Reemplaza con la URL real de tu API
                #headers = {'Content-Type': 'application/json'}
                #response = requests.post(url, headers=headers, data=json_data)
                print("Enviado a la BD del cloud el email " + str(payload["email"]) +" y password" + str(payload["password"]))
                print("---------------------------------------")
            
            else:
                print("ERROR FORMATO!-->PTIN2023/A2/USERINCLOUD")        
        else:
            print("Recibido el texto plano siguiente: "+msg.payload.decode('utf-8'))

#----------------------------------------------------------------------------------------
    if msg.topic == "PTIN2023/A2/USERSAVECLOUD":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['name','email','phone','role', 'password','when']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                url = 'http://127.0.0.1:5000/api/register'  # Reemplaza con la URL real de tu API
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, headers=headers, data=msg.payload)
                if response.status_code == 200:
                   print("CORRECTO ENVIADO")
                else:
                    print("INCORRECTO ENVIADO")

                # Haz algo con el mensaje de error 
                print("Enviado a la BD del cloud el email " + str(payload["email"]) +" y password" + str(payload["password"]))
                print("---------------------------------------")
            
            else:
                print("ERROR FORMATO!-->PTIN2023/A2/USERSAVECLOUD")        
        else:
            print("Recibido el texto plano siguiente: "+msg.payload.decode('utf-8'))

#----------------------------------------------------------------------------------------
    #Hay que poner un tema en común, sinó se petará todo
    if msg.topic == "PTIN2023/A1/DRONE/TOCLOUD/UPDATESTATUS":
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'status']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                
                # Haz algo con el mensaje de error 
                print("Enviado a la BD id_dron " + str(payload["id_dron"]) +" y status" + str(payload["status"]))
                print("---------------------------------------")
            
            else:
                print("PTIN2023/A1/DRONE/TOCLOUD/UPDATESTATUS")        
        else:
            print("Recibido el texto plano siguiente: "+msg.payload.decode('utf-8'))

#----------------------------------------------------------------------------------------
    if msg.topic == "PTIN2023/CAR/UPDATELOCATION":
        if(is_json(msg.payload.decode('utf-8'))):
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_car', 'location_act', 'status', 'status_num', 'battery', 'autonomy']
            #YA EXSITE: license_plate,capacitylast,_maintenance_date,beehive,location_in,location_act,location_end
            if all(key in payload for key in needed_keys):                
                logging.info("update llega aqui siu")
                url = 'http://api:5000/api/UPDATELOCATION'
                response =  requests.post(url, json = payload)
            else: 
                logging.info("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | UPDATELOCATION")

#----------------------------------------------------------------------------------------    
    if msg.topic == "PTIN2023/CAR/UPDATESTATUS":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_car', 'status', 'status_num']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                logging.info("status llega aqui siu")
                url = 'http://api:5000/api/UPDATESTATUS'
                response =  requests.post(url, json = payload)
            else: 
                logging.info("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | UPDATESTATUS")          
#----------------------------------------------------------------------------------------    
    if msg.topic == "PTIN2023/TOCLOUD/DRON_UPDATESTATUS":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron', 'status', 'status_num']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                logging.info("status llega aqui siu")
                url = 'http://api:5000/api/TOCLOUD_UPDATESTATUS'
                response =  requests.post(url, json = payload)
            else: 
                logging.info("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | TOCLOUD_UPDATESTATUS")          
#----------------------------------------------------------------------------------------    
    if msg.topic == "PTIN2023/TOCLOUD/DRON_UPDATELOCATION":#Hay que poner un tema en común, sinó se petará todo
        if(is_json(msg.payload.decode('utf-8'))):
            #tratamiento del mensaje-->
            payload = json.loads(msg.payload.decode('utf-8'))
            needed_keys = ['id_dron','location_act','status','status_num','battery','autonomy']
            #si el mensaje es que que queremos, entonces lo tratamos
            if all(key in payload for key in needed_keys):                
                logging.info("status llega aqui siu")
                url = 'http://api:5000/api/TOCLOUD_UPDATELOCATION'
                response =  requests.post(url, json = payload)
            else: 
                logging.info("SUBNORMAL!!! ENVIA BIEN LOS CAMPOS | TOCLOUD_UPDATELOCATION")          



def start_mqtt_subscriber():
    # Create an MQTT client
    client = mqtt.Client()

    # Set up callback functions
    client.on_connect = on_connect
    client.on_message = on_message

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