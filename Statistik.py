# -*- coding: utf-8 -*-
import Tools
import Tempsensorsteuerung
import math
import time
import threading

runStatistik=True

def setStatistik():
    global runStatistik
    runStatistik=True
    #starte Thread für das warten bis Statistik beendet wird
    thread_temp = threading.Thread(target=__stopStatistik).start()

    print("Werte für Statistik werden abgerufen")
    while runStatistik:
        print("neue Runde")
       ## TempRauchgas = Tempsensorsteuerung.getTempRauchgas()
       ## TempRaum = Tempsensorsteuerung.getTempRaumTemp()

       ## if TempRauchgas < 0:
         ##   TempRauchgas = 0
       ## if TempRaum < 0:
         ##   TempRaum = 0
            
        ## Tools.sendcommand('add 9,1,' + math.ceil(TempRauchgas))
        ##Tools.sendcommand('add 9,2,' + math.ceil(TempRaum))
        ##print("Schreibe Temperatur in Statisktik (Rauchgas):" + TempRauchgas)
        ##print("Schreibe Temperatur in Statisktik (Raum):" + TempRaum)
        Tools.sendcommand("add 9,1,150")
        Tools.sendcommand("add 9,0,100")   
        time.sleep(0.5)


def __stopStatistik():
    global runStatistik
    Tools.leereInputBuffer() #Input Buffer löschen
    if Tools.recievecommand()=="s9b0":
        print("Statistik wurde vom User beendet")
        runStatistik=False
