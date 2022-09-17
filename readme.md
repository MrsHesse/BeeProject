# Test using HiveMQ Websocket Client

## Access the HiveMQ Websocket Client.
https://websocketclient.hivemq.cloud/?username=GreyCourtBees&host=88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud&port=8884

Host : 88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud
Port : 8884
username : GreyCourtBees
password : F1zzBuzz
SSL : checked

Subscribe to : gc-hive/#

Run code on Raspberry Pi - 
>> cd  /home/pi/Documents/Bees
>> python3 pubsensors.py

need to install the libraries
>> sudo pip3 install bme680
>> sudo pip3 install paho.mqtt

pubsensors.py
from paho import mqtt

# broker details - will need to hide these
mqttbroker = "88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud"
mqttport = 8883
mqttuser = "GreyCourtBees"
mqttpwd = "F1zzBuzz"

topic = "gc-hive/BME680"

# setting callbacks for different events to see if it works, print the message etc.
def on_connect(client, userdata, flags, rc, properties=None):
	print("CONNACK received with code %s." % rc)
	if rc != paho.CONNACK_ACCEPTED:
		raise IOError("Couldn't establish a connection with the MQTT server")


def publish_value(client, value):
	result = client.publish(topic=topic, payload=str(value).encode("UTF-8"), qos=2)
	print(f"published to {topic} - {value} [{result}]")
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
client = paho.Client(client_id="", userdata=None, protocol=paho.MQTTv5)
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
        
        data = f"{now} {temp:.2f} {pres:.1f}  {hum:.2f}" 
        print("data -", data)
        publish_value(client, data)
        
        #if sensor.data.heat_stable:
        #    output += f", {sensor.data.gasresitance} ohms"
        #print(output)
        
        time.sleep(5)
        



