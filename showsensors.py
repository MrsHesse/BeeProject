# import the BME680 library for RPI
import bme680

# import time library for delay purposes
import time

# import datetime library for timestamp
from datetime import datetime


# initialise the sensor
sensor = bme680.BME680()

# define the sampling rate for individual paramters
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)

# filter out noises
sensor.set_filter(bme680.FILTER_SIZE_3)

# loop to read data
while True:
    # if data is available    
    if sensor.get_sensor_data():
        now  = datetime.now().strftime("%d-%b-%Y (%H:%M:%S.%f)")
        pres = sensor.data.pressure
        hum = sensor.data.humidity
        temp = sensor.data.temperature
        print(now, temp, pres,hum)
        
        #if sensor.data.heat_stable:
        #    output += f", {sensor.data.gasresitance} ohms"
        #print(output)
        
        time.sleep(5)
        
