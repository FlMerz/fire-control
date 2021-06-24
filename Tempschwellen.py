#---------------------Imports--------------------------
import time
import serial
import Tools

#-----Zuordnung der Tempschwellen Dateien--------------

tempschwelle1_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/schwelle1.txt"           #Pfad der ersten Tempschwelle
tempschwelle2_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/schwelle2.txt"           #Pfad der zweiten Tempschwelle
tempschwelle3_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/schwelle3.txt"           #Pfad der dritten Tempschwelle
tempschwellen_list=[tempschwelle1_File,tempschwelle2_File,tempschwelle3_File]                       #List wo alle Pfade gespeichert sind



#-----------Methods------------------------------------    
def updateTemperaturschwellen():
    tempschwelle1=Tools.ReadFile(tempschwelle1_File)
    tempschwelle2=Tools.ReadFile(tempschwelle2_File)
    tempschwelle3=Tools.ReadFile(tempschwelle3_File)
    Tools.sendcommand('Automatik.n0.val='+tempschwelle1)
    Tools.sendcommand('Automatik.n1.val='+tempschwelle2)
    Tools.sendcommand('Automatik.n2.val='+tempschwelle3)

def Werte_einlesen():
    try:
        for i in range(0,2):
            recieved = Tools.recievecommand()
            print("Datenempfangen: "  + recieved)
            Tools.writeInFile(recieved,tempschwellen_list[i])
    except Exception as e:
        print("Fehler in Tempschwellen.py: Fehler beim Einlesen der Tempschwellen")
        Tools.sendcommand('Error.t1.txt="'+str(e)+'"')

def getValueOfTempschwelle1():
    return int(Tools.ReadFile(tempschwelle1_File))

def getValueOfTempschwelle2():
    return int(Tools.ReadFile(tempschwelle2_File))

def getValueOfTempschwelle3():
    return int(Tools.ReadFile(tempschwelle3_File))

