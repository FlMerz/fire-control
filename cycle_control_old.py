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
                zyklus_thread = threading.Thread(target=__zyklus).start()
                Tools.sendcommand("page Home")
                return
            if recieved=="s12b2":                                   #User drückt zurück Button
                return                        
        else:
            zyklus_thread = threading.Thread(target=__zyklus).start()

    except Exception as e:
        print("Exception in Cyclce_control.py in check preconditions: "+ str(e))
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
        #if phase1ausfuehren:
            #================================= Phase 1 ====================================================
            phase2_wiederholen=True
            while phase2_wiederholen:
                phase2_wiederholen=False
                #Phase 1: Phase beginnt
                #-------------------------
                print("Phase 1 startet")
                flap.phase1()
                currentZyklusPhase =1
                Tools.sendcommand("Home.bt1.val=1")
                Tools.sendcommand("Home.bt2.val=0")
                Tools.sendcommand("Home.bt3.val=0")
                Tools.sendcommand("Home.bt0.val=0")
                
                #Phase 1: wartet auf ende
                #-------------------------
                #print("Phase 1 wartet auf ende")
                if phase1ausfuehren:
                    try:
                        while TempSensor.getTempRauchgas()<TempLimits.getValueOfTempschwelle1():
                            time.sleep(1)
                            if stopZyklus:
                                print("User bricht Zyklus ab")
                                stopZyklus=False
                                raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
                        nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde
                        #=========8======================== Phase 2 ====================================================
                        print("consider delay of templimit")
                        time.sleep(60*TempLimits.getValueOfTempschwelle1delay())
                        print("templimit delay over. proceed with next phase...")
                    except Exception as e:
                        exc_type, exc_obj, exc_tb = sys.exc_info()
                        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                        print(exc_type, fname, exc_tb.tb_lineno)
                        print(sys.exc_info())
                        print("Expection in Phase 1")
                phase1ausfuehren=True

                #Phase 2: Phase beginnt
                #-------------------------
                print("Phase 2 startet")
                flap.phase2()
                currentZyklusPhase = 2
                Tools.sendcommand("Home.bt1.val=0")
                Tools.sendcommand("Home.bt2.val=1")
                Tools.sendcommand("Home.bt3.val=0")
                Tools.sendcommand("Home.bt0.val=0")
                
                #Phase 2: wartet auf ende
                #-------------------------
                #print("Phase 2 wartet auf ende")
                while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle2():                         # Warte bis temp unter 500 Grad sinkt
                    time.sleep(2)
                    if stopZyklus:
                        print("User bricht Zyklus ab")
                        stopZyklus=False
                        raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
                nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde 
                #================================= Phase 3 ====================================================
                print("consider delay of templimit")
                time.sleep(60*TempLimits.getValueOfTempschwelle2delay())
                print("templimit delay over. proceed with next phase...")
                  
                #Phase 3: Phase 3 beginnt
                #-------------------------
                print("Phase 3 startet")
                flap.phase3()
                currentZyklusPhase = 3
                Tools.sendcommand("Home.bt1.val=0")
                Tools.sendcommand("Home.bt2.val=0")
                Tools.sendcommand("Home.bt3.val=1")
                Tools.sendcommand("Home.bt0.val=0")
                #Phase 3: Phase wartet auf ende
                #-------------------------
                print("Phase 3 wartet auf ende")
                while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle3() and phase2_wiederholen==False: # Warte bis temp unter 500 Grad sinkt
                    if stopZyklus:
                        print("User bricht Zyklus ab")
                        stopZyklus=False
                        raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
                    if nachlegen:                     # Wenn Holz nachgelegt wird
                        #if float(Tools.ReadFile(Path_currentTemp))>TempLimits.getValueOfTempschwelle2():                        # Wenn Rauchgas wieder Temperatur von Phase 2 erreicht
                            phase2_wiederholen=True
                            # Phase 2 wird wiederholt
                            nachlegen=False                 #variable wird zurückgesetzt, weil nachlegen gedürckt wurde
                    time.sleep(2)

        #================================= Phase 4 ====================================================
               
            #Phase 4: Phase  beginnt
            #-------------------------
            print("Phase 4 startet")
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

def _executePhase1():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    try:
        while TempSensor.getTempRauchgas()<TempLimits.getValueOfTempschwelle1():
            time.sleep(1)
            if stopZyklus:
                print("User bricht Zyklus ab")
                stopZyklus=False
                raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
        nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde
        #=========8======================== Phase 2 ====================================================
        print("consider delay of templimit")
        time.sleep(60*TempLimits.getValueOfTempschwelle1delay())
        print("templimit delay over. proceed with next phase...")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, fname, exc_tb.tb_lineno)
        print(sys.exc_info())
        print("Expection in Phase 1")

def _executePhase2():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    print("Start Phase 2")
    flap.phase2()
    currentZyklusPhase = 2
    Tools.sendcommand("Home.bt1.val=0")
    Tools.sendcommand("Home.bt2.val=1")
    Tools.sendcommand("Home.bt3.val=0")
    Tools.sendcommand("Home.bt0.val=0")
    print("Phase 2 wait for end")
    while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle2():                         # Warte bis temp unter 500 Grad sinkt
        time.sleep(2)
        if stopZyklus:
            print("User bricht Zyklus ab")
            stopZyklus=False
            raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
    nachlegen=False                         #variable wird zurückgesetzt, weil evtl. nachlegen gedrückt wurde 
    print("consider delay of templimit")
    time.sleep(60*TempLimits.getValueOfTempschwelle2delay())
    print("Phase 3 delay time over. Phase 3 will end")

def _executePhase3():
    global stopZyklus
    global nachlegen
    global phase2_wiederholen
    global phase1ausfuehren
    print("Start Phase 3")
    flap.phase3()
    currentZyklusPhase = 3
    Tools.sendcommand("Home.bt1.val=0")
    Tools.sendcommand("Home.bt2.val=0")
    Tools.sendcommand("Home.bt3.val=1")
    Tools.sendcommand("Home.bt0.val=0")
    #Phase 3: Phase wartet auf ende
    #-------------------------
    print("Phase 3 waiting for end")
    while TempSensor.getTempRauchgas()>TempLimits.getValueOfTempschwelle3() and phase2_wiederholen==False: # Warte bis temp unter 500 Grad sinkt
        if stopZyklus:
            print("User bricht Zyklus ab")
            stopZyklus=False
            raise Exception                 #Werfe Exception wenn Nutzer Zyklus abbricht
        if nachlegen:                     # Wenn Holz nachgelegt wird
            #if float(Tools.ReadFile(Path_currentTemp))>TempLimits.getValueOfTempschwelle2():                        # Wenn Rauchgas wieder Temperatur von Phase 2 erreicht
                phase2_wiederholen=True
                # Phase 2 wird wiederholt
                nachlegen=False                 #variable wird zurückgesetzt, weil nachlegen gedürckt wurde
        time.sleep(2)

def _executePhase4():
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
        
def _checkingPreconditions():
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
            zyklus_thread = threading.Thread(target=__zyklus).start()
            Tools.sendcommand("page Home")
            return
        if recieved=="s12b2":                                   #User drückt zurück Button
            return     
    else:
        print("Start Temperatur is smaller then templimit 3. Start Cyclus Phase 1")
        zyklus_thread = threading.Thread(target=__zyklus).start()
