# -*- coding: utf-8 -*-

#----------Metadata--------------------------------
#This script is responsible for the auto cycle modus.
#
#----------Imports--------------------------------
import serial
import time
import Tools
import flap_control as flap
import threading
import temperature_limits as TempLimits
import sys,os
import sensor_temperature_control as TempSensor

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
        _checkingStartconditions()
    except Exception as e:
        print("Exception in Cyclce_control.py in check preconditions: "+ str(e))
        Tools.sendcommand('Error.t1.txt="'+str(e)+'"')
        Tools.sendcommand("bt4.val=0")          #set Button back to not activated
        Tools.sendcommand("tsw bt1,1")
        Tools.sendcommand("tsw bt2,1")
        Tools.sendcommand("tsw bt3,1")
        Tools.sendcommand("tsw bt0,1")


def __zyklus():
    global currentZyklusPhase
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    print("Auto-Zyklus wird gestartet")
    currentZyklusPhase=0
    Tools.sendcommand("tsw bt1,0")
    Tools.sendcommand("tsw bt2,0")
    Tools.sendcommand("tsw bt3,0")
    Tools.sendcommand("tsw bt0,0")
    try:
        #if phase1ausfuehren:
            phase2_wiederholen=True
            while phase2_wiederholen:
                phase2_wiederholen=False
                #Phase 1: starting
                #-------------------------
                if phase1ausfuehren:
                    _handlePhase1()
                phase1ausfuehren=True
                #Phase 2: starting
                #-------------------------
                _handlePhase2()
                #Phase 3: starting
                #-------------------------
                _handlePhase3() 
            #Phase 4: starting
            #-------------------------
            _handlePhase4()
            
    except Exception as e:
        print("Fehler in Zyklussteuerung:")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(sys.exc_info())
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
       ## flap.phase4() -> not used anymore, clap should keep position and shouldnt close completly
        print("Current Phase: " + str(currentZyklusPhase))
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

def _handlePhase1():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    global currentZyklusPhase
    
    print("Phase 1 startet")
    flap.phase1()
    currentZyklusPhase =1
    Tools.sendcommand("Home.bt1.val=1")
    Tools.sendcommand("Home.bt2.val=0")
    Tools.sendcommand("Home.bt3.val=0")
    Tools.sendcommand("Home.bt0.val=0")
    print("Phase 1 wait for end")
    while TempSensor.getTempRauchgas()<TempLimits.getValueOfTempschwelle1():
        time.sleep(1)
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                 #Werfe Exception wenn Nutzer Zyklus abbricht
    nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde
    print("consider delay of templimit")
    counter = 0
    maxcounter  = 60*TempLimits.getValueOfTempschwelle1delay()
    while counter<maxcounter:
        time.sleep(1)
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                 #Werfe Exception wenn Nutzer Zyklus abbrichtif stopZykl
        counter += 1
    print("Phase 1 delay time over. Phase 1 will end")

def _handlePhase2():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    global currentZyklusPhase
    print("Start Phase 2")
    flap.phase2()
    currentZyklusPhase = 2
    Tools.sendcommand("Home.bt1.val=0")
    Tools.sendcommand("Home.bt2.val=1")
    Tools.sendcommand("Home.bt3.val=0")
    Tools.sendcommand("Home.bt0.val=0")
    print("Phase 2 wait for end")
    while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle2():                         # Warte bis temp unter 500 Grad sinkt
        time.sleep(1)
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                  #Werfe Exception wenn Nutzer Zyklus abbricht
    nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde 
    print("consider delay of templimit")
    counter = 0
    maxcounter  = 60*TempLimits.getValueOfTempschwelle1delay()
    while counter<maxcounter:
        time.sleep(1)
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                 #Werfe Exception wenn Nutzer Zyklus abbrichtif stopZykl
        counter += 1
    print("Phase 2 delay time over. Phase 2 will end")

def _handlePhase3():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    global currentZyklusPhase
    print("Start Phase 3")
    flap.phase3()
    currentZyklusPhase = 3
    Tools.sendcommand("Home.bt1.val=0")
    Tools.sendcommand("Home.bt2.val=0")
    Tools.sendcommand("Home.bt3.val=1")
    Tools.sendcommand("Home.bt0.val=0")
    print("Phase 3 waiting for end")
    while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle3() and phase2_wiederholen==False: # Warte bis temp unter 500 Grad sinkt
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                 #Werfe Exception wenn Nutzer Zyklus abbricht
        if nachlegen:                     # Wenn Holz nachgelegt wird
                phase2_wiederholen=True
                nachlegen=False                 #variable wird zurückgesetzt, weil nachlegen gedürckt wurde
        time.sleep(1)
    print("consider delay of templimit")
    counter = 0
    maxcounter  = 60*TempLimits.getValueOfTempschwelle1delay()
    while counter<maxcounter:
        time.sleep(1)
        if stopZyklus:
            stopZyklus=False
            raise Exception("User has stopped Cycle")                 #Werfe Exception wenn Nutzer Zyklus abbrichtif stopZykl
        counter += 1
    print("Phase 3 delay time over. Phase 3 will end")

def _handlePhase4():
    global currentZyklusPhase
    print("Start Phase 4")
    flap.phase4()
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
        
def _checkingStartconditions():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    global currentZyklusPhase
    print("Checking Preconditions...")
    if TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle3(): 
        Tools.sendcommand("page Zustand")                               #Seite Zustand anzeigen
        recieved = Tools.recievecommand()
        if recieved=="s12b0":                                          #Aufheizen wurde gedrückt -> gehe zu Phase 1 
           zyklus_thread = threading.Thread(target=__zyklus).start()
           Tools.sendcommand("page Home")
           return
        if recieved=="s12b1":                                          # Abheizen wurde gedrückt
            phase1ausfuehren=False
            print("Abheizen wurde gedrückt. Skip Phase 1")
            zyklus_thread = threading.Thread(target=__zyklus).start()
            Tools.sendcommand("page Home")
            return
        if recieved=="s12b2":                                   #User drückt zurück Button
            return     
    else:
        print("Start Temperatur is smaller then templimit 3. Start Cyclus Phase 1")
        zyklus_thread = threading.Thread(target=__zyklus).start()
