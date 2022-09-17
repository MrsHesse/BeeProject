# Explination of data collection and sharing approach
[see slides](https://docs.google.com/presentation/d/1-Z-34nL_-e_dLuUNPXYTUxwACRXUNZZtR-lcUro-GA0/edit?usp=sharing)

# To Test using HiveMQ Websocket Client

1. Access the HiveMQ Websocket Client.
https://websocketclient.hivemq.cloud/?username=GreyCourtBees&host=88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud&port=8884

2. Fill in credentials - these have been removed here for security.
- Host : 88d7c3c9d32f4c10aeb6593c796b8654.s1.eu.hivemq.cloud
- Port : 8884
- username : ****
- password : ****
- SSL : checked

3. Subscribe to : gc-hive/#

# other info
## To run code on Raspberry Pi - 
>> cd  <path>
>> python3 pubsensors.py

## need to install the libraries
>> sudo pip3 install bme680
>> sudo pip3 install paho.mqtt

