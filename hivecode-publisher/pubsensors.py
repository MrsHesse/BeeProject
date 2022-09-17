# import the BME680 library for RPI
import bme680

# import time library for delay purposes
import time

# import datetime library for timestamp
from datetime import datetime

import json

# import paho mqtt libraries to publish sensor data
import paho.mqtt.client as paho
from paho import mqtt

# broker details - for security these are hidden and need to be included for code to work
mqttbroker = "88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud"
mqttport = 8883
mqttuser = "****"
mqttpwd = "****"

#topic = "gc-hive/BME680"
#topic = "Bee/Data"
topic_temp = "gc-hive/temperature"
topic_hum = "gc-hive/humidity"
topic_pres = "gc-hive/pressure"

# sample time in seconds
sample_time = 30

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
	print("CONNACK received with code %s." % rc)
	if rc != paho.CONNACK_ACCEPTED:
		raise IOError("Couldn't establish a connection with the MQTT server")



def publish_value(client, topic, value):
	
    data = { "time"  : datetime.now().isoformat(),
             "value" : value}
            
    jsonstr = json.dumps(data)
    
    result = client.publish(topic=topic, payload=jsonstr, qos=2)
    print("P", f"published to {topic} --> {jsonstr} [{result}]")
    print()
    return result


# initialise the sensor
sensor = bme680.BME680()

# define the sampling rate for individual paramters
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

# filter out noises
sensor.set_filter(bme680.FILTER_SIZE_3)


# initialise the MQTT client

# create the client
#client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
client = paho.Client("p2")
client.on_connect = on_connect

# enable TLS for secure connection
client.tls_set(tls_version=mqtt.client.ssl.PROTOCOL_TLS)

# set username and password
client.username_pw_set(mqttuser, mqttpwd)

# connect to HiveMQ Cloud on port 8883 (default for MQTT)
client.connect(mqttbroker, mqttport)

client.loop_start()

# loop to read data from sensors and publish
while True:
    # if data is available    
    if sensor.get_sensor_data():
        now  = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        pres = sensor.data.pressure
        hum = sensor.data.humidity
        temp = sensor.data.temperature
        
        
        #publish_value(client, topic, data)
        publish_value(client, topic_temp, temp)
        publish_value(client, topic_hum, hum)
        publish_value(client, topic_pres, pres)
        
        #if sensor.data.heat_stable:
        #    output += f", {sensor.data.gasresitance} ohms"
        #print(output)
        
        time.sleep(sample_time)
        
