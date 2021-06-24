
import Tools
import time
import max31855_library as max

#-----------allgemeine Einstellungen---------------
Messverzoegerung = 5        # Wie viel Sekunden Pause gemacht werden soll nach jeder Messung



#-----------Raumtempsensor Port Deklaration--------

CS_RaumTemp = 27
SCK_RaumTemp = 22
SO_RaumTemp= 17
units_RaumTemp = "c" #alternativ geht auf Fahrenheit


#---------------Methoden---------------------------------
##def getTempRauchgas():
##    temp=thermocouple_Rauchgas.get()
##    #thermocouple.cleanup()
##    return temp

while True:
    thermocouple_RaumTemp = max.MAX31855(CS_RaumTemp, SCK_RaumTemp, SO_RaumTemp ,units_RaumTemp)
    print(thermocouple_RaumTemp.get())
    time.sleep(5)
