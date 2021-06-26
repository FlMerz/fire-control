# -*- coding: utf-8 -*-


#----------------Metadaten----------------
#this Script is mainly responsible for the motor-controle.
#It provides several methods which can be used to controle the motor


#-------------Imports--------------------------------
import stepper_self as stepper
import Tools


#---------globale Definitionen------------------------
File_Phase="/home/pi/Desktop/FireControl/Daten/Aktuelle_Phase/Phase.txt"
StepsProPhase=30

#-------------Methoden----------------------------------

def Kalibrieren():
    stepper.rotate_clockwise(StepsProPhase * 3)
    Tools.writeInFile("4",File_Phase)                               #Phase in File aktualsieren

def phase1():
    print("Motor fährt in Phase 1...")
    aktuellePhase = Tools.ReadFile(File_Phase)
    if aktuellePhase =="4":
        stepper.rotate_counterwise(StepsProPhase * 3)      #Motor in Stellung verfahren
        Tools.writeInFile("1",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="3":
        stepper.rotate_counterwise(StepsProPhase * 2)      #Motor in Stellung verfahren
        Tools.writeInFile("1",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="2":
        stepper.rotate_counterwise(StepsProPhase)          #Motor in Stellung verfahren
        Tools.writeInFile("1",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="1":
        return

def phase2():
    print("Motor fährt in Phase 2...")
    aktuellePhase = Tools.ReadFile(File_Phase)
    if aktuellePhase =="4":
        stepper.rotate_counterwise(StepsProPhase*2)      #Motor in Stellung verfahren
        Tools.writeInFile("2",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="3":
        stepper.rotate_counterwise(StepsProPhase)      #Motor in Stellung verfahren
        Tools.writeInFile("2",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="1":
        stepper.rotate_clockwise(StepsProPhase)          #Motor in Stellung verfahren
        Tools.writeInFile("2",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="2":
        return

    
def phase3():
    print("Motor fährt in Phase 3...")
    aktuellePhase = Tools.ReadFile(File_Phase)
    if aktuellePhase =="4":
        stepper.rotate_counterwise(StepsProPhase)      #Motor in Stellung verfahren
        Tools.writeInFile("3",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="2":
        stepper.rotate_clockwise(StepsProPhase)      #Motor in Stellung verfahren
        Tools.writeInFile("3",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="1":
        stepper.rotate_clockwise(StepsProPhase*2)          #Motor in Stellung verfahren
        Tools.writeInFile("3",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="3":
        return


def phase4():
    print("Motor fährt in Phase 4...")
    aktuellePhase = Tools.ReadFile(File_Phase)
    if aktuellePhase =="3":
        stepper.rotate_clockwise(StepsProPhase)      #Motor in Stellung verfahren
        Tools.writeInFile("4",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="2":
        stepper.rotate_clockwise(StepsProPhase * 2)      #Motor in Stellung verfahren
        Tools.writeInFile("4",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="1":
        stepper.rotate_clockwise(StepsProPhase * 3)          #Motor in Stellung verfahren
        Tools.writeInFile("4",File_Phase)                           #Phase in File aktualsieren
        return
    if aktuellePhase =="4":
        return
