import paho.mqtt.client as mqtt
import json


# Crea un objeto cliente MQTT
#client = mqtt.Client()

# Conecta al servidor MQTT
#client.connect("test.mosquitto.org", 1883 , 60)


#------------
# Crea un objeto cliente MQTT
client = mqtt.Client()

# Conecta al servidor MQTT
client.connect("localhost", 1883 , 60)

# Crea un mensaje JSON
mensaje = {    "id_dron": 436703853, 
           "status": "STOP"
       }

# Codifica el mensaje JSON a una cadena
mensaje_json = json.dumps(mensaje)

# Publica el mensaje en el topic "PTIN2023/A1/CAR"
client.publish("PTIN2023/A2/FRAN/CLOUD", mensaje_json)

print("ENVIADO")
# Cierra la conexión MQTT
client.disconnect()
#------------
# Crea un mensaje JSON
#mensaje = {"CoordenadaX": 25, "CoordenadaY": 60}
#mensaje3 = {"KEY1": "25", "KEY2": "123", "KEY3": "60"}

#mensaje2="WORK DONE BY OMAR B & JOAQUIM H u.u"

# Codifica el mensaje JSON a una cadena
#mensaje_json = json.dumps(mensaje3)

# Publica el mensaje en el topic "mi/topic/json"
#client.publish("PTIN2023/A2/TOCLOUD", mensaje_json)

# Cierra la conexión MQTT
#client.disconnect()