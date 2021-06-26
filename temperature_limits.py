#---------------------Imports--------------------------
import time
import serial
import Tools

#-----Zuordnung der Tempschwellen Dateien--------------

tempschwelle1_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit1.txt"           #Pfad der ersten Tempschwelle
tempschwelle2_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit2.txt"           #Pfad der zweiten Tempschwelle
tempschwelle3_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit3.txt"           #Pfad der dritten Tempschwelle
tempschwelle1delay_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit1delay.txt"           #Pfad der ersten Tempschwelle
tempschwelle2delay_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit2delay.txt"           #Pfad der zweiten Tempschwelle
tempschwelle3delay_File="/home/pi/Desktop/FireControl/Daten/Temperaturschwellen/templimit3delay.txt"           #Pfad der dritten Tempschwelle
tempschwellen_list=[tempschwelle1_File,tempschwelle2_File,tempschwelle3_File,tempschwelle1delay_File,tempschwelle2delay_File,tempschwelle3delay_File]                       #List wo alle Pfade gespeichert sind



#-----------Methods------------------------------------    
def updateTemperaturschwellen():
    tempschwelle1=Tools.ReadFile(tempschwelle1_File)
    tempschwelle2=Tools.ReadFile(tempschwelle2_File)
    tempschwelle3=Tools.ReadFile(tempschwelle3_File)
    tempschwelle1delay=Tools.ReadFile(tempschwelle1delay_File)
    tempschwelle2delay=Tools.ReadFile(tempschwelle2delay_File)
    tempschwelle3delay=Tools.ReadFile(tempschwelle3delay_File)
    Tools.sendcommand('Automatik.n0.val='+tempschwelle1)
    Tools.sendcommand('Automatik.n1.val='+tempschwelle2)
    Tools.sendcommand('Automatik.n2.val='+tempschwelle3)
    Tools.sendcommand('Automatik.n4.val='+tempschwelle1delay)
    Tools.sendcommand('Automatik.n5.val='+tempschwelle2delay)
    Tools.sendcommand('Automatik.n6.val='+tempschwelle3delay)

def Werte_einlesen():
    try:
        for i in range(0,6):
            recieved = Tools.recievecommand()
            print("Datenempfangen: "  + recieved)
            Tools.writeInFile(recieved,tempschwellen_list[i])
    except Exception as e:
        print("Fehler in Tempschwellen.py: Fehler beim Einlesen der Tempschwellen")
        Tools.sendcommand('Error.t1.txt="'+str(e)+'"')

def getValueOfTempschwelle1():
    return float(Tools.ReadFile(tempschwelle1_File))

def getValueOfTempschwelle2():
    return float(Tools.ReadFile(tempschwelle2_File))

def getValueOfTempschwelle3():
    return float(Tools.ReadFile(tempschwelle3_File))

def getValueOfTempschwelle1delay():
    return float(Tools.ReadFile(tempschwelle1delay_File))

def getValueOfTempschwelle2delay():
    return float(Tools.ReadFile(tempschwelle2delay_File))

def getValueOfTempschwelle3delay():
    return float(Tools.ReadFile(tempschwelle3delay_File))

