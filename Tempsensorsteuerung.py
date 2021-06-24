# -*- coding: utf-8 -*-
#!/usr/bin/python

#---------Imports----------------------

import Tools
import time
import max31855_library as max

#-----------allgemeine Einstellungen---------------
Messverzoegerung = 5         # Wie viel Sekunden Pause gemacht werden soll nach jeder Messung

#-----------Rauchgastempsensor Port Deklaration--------
CS_Rauchgas = 27
SCK_Rauchgas = 22
SO_Rauchgas= 17
units_Rauchgas = "c" #alternativ geht auf Fahrenheit

#-----------Raumtempsensor Port Deklaration--------

CS_RaumTemp = 3
SCK_RaumTemp = 4
SO_RaumTemp= 2
units_RaumTemp = "c" #alternativ geht auf Fahrenheit

#-------------RauchGasTemperatur File ------------------
Path_currentTemp = "/home/pi/Desktop/FireControl/Daten/currentTempGas.txt"

#---------------Methoden---------------------------------
def getTempRauchgas():
    thermocouple_Rauchgas = max.MAX31855(CS_Rauchgas, SCK_Rauchgas, SO_Rauchgas ,units_Rauchgas)
    temp=thermocouple_Rauchgas.get()
    #thermocouple.cleanup()
    return temp

def getTempRaumTemp():
    thermocouple_RaumTemp = max.MAX31855(CS_RaumTemp, SCK_RaumTemp, SO_RaumTemp ,units_RaumTemp)
    temp=thermocouple_RaumTemp.get()
    #thermocouple.cleanup()
    return temp


def updateTemperatur():
    while True:
        try:
            gastemp = str(getTempRauchgas())
            #get Temperatur für Abgastemperatur
            Tools.sendcommand('Home.t1.txt="'+gastemp+'"')
            Tools.writeInFile(gastemp,Path_currentTemp) 
            print("Rauchgastemperatursensor: " + gastemp)
        except Exception as e:
            print("Rauchgastemperatursensor: Fehler bei Messung: "+ str(e))
            Tools.sendcommand('Home.t1.txt="-"')
            
        try:    
            #get Temperatur für Raumtemperatur
            Tools.sendcommand('Home.t0.txt="'+str(getTempRaumTemp())+'"')
            print("Raumtemperatursensor: " + str(getTempRaumTemp()))
            print("-----------------------------")
        except Exception as e:
            print("Raumtemperatursensor: Fehler bei Messung: " + str(e))
            print("-----------------------------")
            Tools.sendcommand('Home.t0.txt="-"')
        time.sleep(Messverzoegerung) #Zeit wie oft in der Sekunde die Temperatur aktualisiert werden soll
