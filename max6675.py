import time

import MAX6675.MAX6675 as MAX6675


# Define a function to convert celsius to fahrenheit.
#def c_to_f(c):
#       return c * 9.0 / 5.0 + 32.0

# Raspberry Pi software SPI configuration.
SCK = 2
CS  = 3
SO  = 4
sensor = MAX6675.MAX6675(SCK, CS, SO)

# Raspberry Pi hardware SPI configuration.
#SPI_PORT   = 0
#SPI_DEVICE = 0
#sensor = MAX6675.MAX6675(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

def getTempMAX6675():
    return sensor.readTempC()

# Loop printing measurements every second.
#while True:
#	temp = sensor.readTempC()
#	print(temp)
#	print("Thermocouple Temperature: ".format(temp, c_to_f(temp)))
#	time.sleep(1.0)
