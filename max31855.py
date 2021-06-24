#!/usr/bin/python
import max31855_library as max

CS = 9
SCK = 10
SO= 11
units = "c" #alternativ geht auf Fahrenheit
thermocouple = max.MAX31855(CS, SCK, SO ,units)

def getTempMAX31855():
    temp=thermocouple.get()
    #thermocouple.cleanup()
    return temp
