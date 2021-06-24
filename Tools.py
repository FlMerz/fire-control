# -*- coding: utf-8 -*-
import serial

#----serielle Verbindung über UART----------------
ser = serial.Serial("/dev/serial0")   #Serielle Verbindung aufbauen
ser.baudrate = 9600                   #Baudrate festlegen





#-------------Methods---------------------------

def recievecommand():                           #Wartet bis ein Befehl von dem Nextion Display gesendet wird
    value_undecoded=ser.readline()
    print(value_undecoded)
    value_decoded=value_undecoded.decode()[:-2]
    return value_decoded


def leereInputBuffer():
    ser.flushInput() 

def sendcommand(command):                       #Sendet Kommando an Nextion Display
    if ser.isOpen():
        ser.write(command.encode())
        ser.write(b'\xFF\xFF\xFF')


def ReadFile(File_Path):
    with open(File_Path) as file:
        value=file.readline()
    return value

def writeInFile(text, path_file):
    file = open(path_file, "w")
    file.write(text)
    file.close()
