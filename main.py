# -*- coding: utf-8 -*-
import serial
import threading
import time
import Zyklussteuerung
import Tempschwellen
import Klappensteuerung
import Tools
import Tempsensorsteuerung
import Statistik
import os 
from subprocess import call                        
                           
###################  Main ################################

#Kalibrierungslauf
Tools.sendcommand('Boot.t0.txt="kalibrierung..."')   #Bootfenster kalibrieren anzeigen
Klappensteuerung.Kalibrieren()
time.sleep(4)
Tools.sendcommand("page Home")                  #Home Screen anzeigen
Tools.sendcommand("bt0.val=1")
Tools.sendcommand("bt1.val=0")
Tools.sendcommand("bt2.val=0")
Tools.sendcommand("bt3.val=0")
Tools.sendcommand("bt4.val=0")
Tools.leereInputBuffer()                    #Input Buffer löschen

#starte Thread für das ständige updaten der Temperaturanzeige
thread_temp = threading.Thread(target=Tempsensorsteuerung.updateTemperatur).start()


#Daten empfangen und darauf reagieren
while True:
    try:
        print("wait for command")
        # ser.inWaiting() > 0:
        recieved_command=Tools.recievecommand()
        print("------------------")
        print(recieved_command)
    
        #---------s2b1: Automatik Settings öffnen   ------------------
        if recieved_command=="s2b1":        #Automatik Settings
            print("Automatik Settings Werte holen")
            Tempschwellen.updateTemperaturschwellen()      #Temperaturschwellen updaten

        #---------s2b2: Open Statistik ----------------------
        if recieved_command=="s2b2":
            print("Open Statistik")
            Statistik.setStatistik()


        #---------s3b0: Automatik Settings Werte einlesen ------------------
        if recieved_command=="s3b0":        #Automatik Settings
           print("Automatik Settings Werte einlesen")
           Tempschwellen.Werte_einlesen()     #Temperaturschwellen einlesen

        
        #---------s0b4: Zyklus starten ----------------------
        if recieved_command=="s0b4":
            #starte Zyklus in neuem Thread
            Zyklussteuerung.starteZyklus()

        #---------s11b0: Zyklus abbrechen ----------------------
        if recieved_command=="s11b0":
            Zyklussteuerung.stoppeZyklus()

        #---------s11b2: Holz nachlegen ----------------------
        if recieved_command=="s11b2":
            Zyklussteuerung.nachlegen_triggern()


        #---------s0b1: manuell Phase 1 ansteuern ----------------------
        if recieved_command=="s0b1":
            Klappensteuerung.phase1()

        #---------s0b2: manuell Phase 2 ansteuern ----------------------
        if recieved_command=="s0b2":
            Klappensteuerung.phase2()

        #---------s0b3: manuell Phase 3 ansteuern ----------------------
        if recieved_command=="s0b3":
            Klappensteuerung.phase3()   

        #---------s0b0: manuell Phase 4 ansteuern ----------------------
        if recieved_command=="s0b0":
            Klappensteuerung.phase4()
            
        #---------s14b1: Lösche Error Log ----------------------
        if recieved_command=="s14b1":
            print("Lösche Error Log")

        #---------s10b1: Fahre Raspi herunter ----------------------
        if recieved_command=="s10b1":
            print("Raspi wird heruntergefahren")
            call("sudo nohup shutdown -h now", shell=True)


        Tools.leereInputBuffer() #Input Buffer löschen
    except Exception as e:
        print("Fehler in main:")
        Tools.sendcommand('Error.t1.txt="'+str(e)+'"')
        print(str(e))
        Tools.leereInputBuffer() #Input Buffer löschen
        #Alle Knöpfe ausschalten
        Tools.sendcommand("Home.bt0.val=0")
        Tools.sendcommand("Home.bt1.val=0")
        Tools.sendcommand("Home.bt2.val=0")
        Tools.sendcommand("Home.bt3.val=0")
        Tools.sendcommand("Home.bt4.val=0")
