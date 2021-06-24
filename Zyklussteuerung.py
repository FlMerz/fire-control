# -*- coding: utf-8 -*-

#----------Metadata--------------------------------
#This script is responsible for the auto cycle modus.
#
#----------Imports--------------------------------
import serial
import time
import Tools
import Klappensteuerung
import threading
import Tempschwellen

#------globale Attribute-----------------------------
stopZyklus=False
nachlegen=False
temperatur=100              #wird nur solange verwendet wie noch kein sensor angeschlossen ist
phase2_wiederholen=True
phase1ausfuehren=True       #variable ändert sich, wenn bestimmte Phasen überspringt werden sollen

Path_currentTemp = "/home/pi/Desktop/FireControl/Daten/currentTempGas.txt"


#----------Methods------------------------------------
def starteZyklus():
    try:
        global phase1ausfuehren
        #================================= Vorbedingungen prüfen ====================================================
        print("Vorbedingungen werden geprüft")
        try:
            currentTemp=int(Tools.ReadFile(Path_currentTemp))               #Read current Temp 
        except Exception as e:
            raise Exception("Aktuelle Rauchgas Temperatur konnte nicht aus Datei gelesen werden")
        
        if currentTemp >Tempschwellen.getValueOfTempschwelle3(): 
            Tools.sendcommand("page Zustand")                               #Seite Zustand anzeigen
            recieved = Tools.recievecommand()
            if recieved=="s12b0":                                          #Aufheizen wurde gedrückt -> gehe zu Phase 1 
               zyklus_thread = threading.Thread(target=__zyklus).start()
               Tools.sendcommand("page Home")
               return
            if recieved=="s12b1":                                          # Abheizen wurde gedrückt
                phase1ausfuehren=False
                zyklus_thread = threading.Thread(target=__zyklus).start()
                Tools.sendcommand("page Home")
                return
            if recieved=="s12b2":                                   #User drückt zurück Button
                return
                    
        else:
            zyklus_thread = threading.Thread(target=__zyklus).start()

    except Exception as e:
        print("Fehler in Zyklussteuerung.py: "+ str(e))
        Tools.sendcommand('Error.t1.txt="'+str(e)+'"')
        Tools.sendcommand("bt4.val=0")          #set Button back to not activated
        Tools.sendcommand("tsw bt1,1")
        Tools.sendcommand("tsw bt2,1")
        Tools.sendcommand("tsw bt3,1")
        Tools.sendcommand("tsw bt0,1")


def __zyklus():
    currentZyklusPhase=0
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    print("Auto-Zyklus wird gestartet")
    Tools.sendcommand("tsw bt1,0")
    Tools.sendcommand("tsw bt2,0")
    Tools.sendcommand("tsw bt3,0")
    Tools.sendcommand("tsw bt0,0")
    try:
        if phase1ausfuehren:
            #================================= Phase 1 ====================================================
            
            #Phase 1: Phase beginnt
            #-------------------------
            print("Phase 1 startet")
            Klappensteuerung.phase1()
            currentZyklusPhase =1
            Tools.sendcommand("Home.bt1.val=1")
            Tools.sendcommand("Home.bt2.val=0")
            Tools.sendcommand("Home.bt3.val=0")
            Tools.sendcommand("Home.bt0.val=0")
            
            #Phase 1: wartet auf ende
            #-------------------------
            print("Phase 1 wartet auf ende")
            while int(Tools.ReadFile(Path_currentTemp))<Tempschwellen.getValueOfTempschwelle1():                         # Warte bis temp unter 500 Grad sinkt
                time.sleep(1)
                if stopZyklus:
                    print("User bricht Zyklus ab")
                    stopZyklus=False
                    raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
            nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde
            #================================= Phase 2 ====================================================
        phase2_wiederholen=True       
        while phase2_wiederholen:
            phase1ausfuehren=True
            phase2_wiederholen=False
            #Phase 2: Phase beginnt
            #-------------------------
            print("Phase 2 startet")
            Klappensteuerung.phase2()
            currentZyklusPhase = 2
            Tools.sendcommand("Home.bt1.val=0")
            Tools.sendcommand("Home.bt2.val=1")
            Tools.sendcommand("Home.bt3.val=0")
            Tools.sendcommand("Home.bt0.val=0")
            
            #Phase 2: wartet auf ende
            #-------------------------
            print("Phase 2 wartet auf ende")
            while int(Tools.ReadFile(Path_currentTemp))>Tempschwellen.getValueOfTempschwelle2():                         # Warte bis temp unter 500 Grad sinkt
                time.sleep(2)
                if stopZyklus:
                    print("User bricht Zyklus ab")
                    stopZyklus=False
                    raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
            nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde 
            #================================= Phase 3 ====================================================

              
            #Phase 3: Phase 3 beginnt
            #-------------------------
            print("Phase 3 startet")
            Klappensteuerung.phase3()
            currentZyklusPhase = 3
            Tools.sendcommand("Home.bt1.val=0")
            Tools.sendcommand("Home.bt2.val=0")
            Tools.sendcommand("Home.bt3.val=1")
            Tools.sendcommand("Home.bt0.val=0")
            


            #Phase 3: Phase wartet auf ende
            #-------------------------
            print("Phase 3 wartet auf ende")
            while int(Tools.ReadFile(Path_currentTemp))>Tempschwellen.getValueOfTempschwelle3() and phase2_wiederholen==False: # Warte bis temp unter 500 Grad sinkt
                if stopZyklus:
                    print("User bricht Zyklus ab")
                    stopZyklus=False
                    raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
                if nachlegen:                     # Wenn Holz nachgelegt wird
                    if int(Tools.ReadFile(Path_currentTemp))>Tempschwellen.getValueOfTempschwelle2():                        # Wenn Rauchgas wieder Temperatur von Phase 2 erreicht
                        phase2_wiederholen=True         # Phase 2 wird wiederholt
                        nachlegen=False                 #variable wird zurückgesetzt, weil nachlegen gedürckt wurde
                        
                time.sleep(2)

        #================================= Phase 4 ====================================================
       
        #Phase 4: Phase  beginnt
        #-------------------------
        print("Phase 4 startet")
        Klappensteuerung.phase4()
        currentZyklusPhase = 4
        Tools.sendcommand("Home.bt3.val=0")
        Tools.sendcommand("Home.bt0.val=1")
        Tools.sendcommand("Home.bt2.val=0")
        Tools.sendcommand("Home.bt1.val=0")
        Tools.sendcommand("Home.bt4.val=0")
        Tools.sendcommand("tsw bt1,1")
        Tools.sendcommand("tsw bt2,1")
        Tools.sendcommand("tsw bt3,1")
        print("Zyklus beendet")
        
    except Exception as e:
        print("Fehler in Zyklussteuerung:")
        print(str(e))
        print("Zyklus wurde gestoppt!")
        stopZyklus=False
        nachlegen=False
        #Alle Knöpfe ausschalten
        Tools.sendcommand("page Home")
        Tools.sendcommand("Home.bt0.val=0")
        Tools.sendcommand("Home.bt1.val=0")
        Tools.sendcommand("Home.bt2.val=0")
        Tools.sendcommand("Home.bt3.val=0")
        Tools.sendcommand("Home.bt4.val=0")
       ## Klappensteuerung.phase4() -> not used anymore, clap should keep position and shouldnt close completly
        if currentZyklusPhase == 1:
            Tools.sendcommand("Home.bt1.val=1")
        if currentZyklusPhase == 2:
            Tools.sendcommand("Home.bt2.val=1")
        if currentZyklusPhase == 3:
            Tools.sendcommand("Home.bt3.val=1")
        if currentZyklusPhase == 4:
            Tools.sendcommand("Home.bt0.val=1")

def stoppeZyklus():
    global stopZyklus
    stopZyklus = True
    

def nachlegen_triggern():
    global nachlegen
    print("Nachlegen wurde getriggert")
    nachlegen=True
    Tools.sendcommand("Home.bt4.val=1")                     #Zyklus Button geht aus nachdem er einmal gedrückt worden ist, da er aber noch  an sein soll wir er hier nochmal angeschaltet
    Tools.sendcommand("page Home")
    
