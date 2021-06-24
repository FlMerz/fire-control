#-------------- Imports-------------------------------------
import RPi.GPIO as GPIO
import time

#----------PIN Declaration-----------------------------------
stepperMotor_PIN1 = 12          #Pin1 motor
stepperMotor_PIN2 = 16          #Pin2 motor
stepperMotor_PIN3 = 20          #Pin3 motor
stepperMotor_PIN4 = 21          #Pin4 motor
endschalter_PIN = 37            #Pin of trigger for calibration

speed=0.002                     # How fast the motor should turn around
error_LED=23


#-------------GPIO Initialization-----------------------------
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(stepperMotor_PIN1,GPIO.OUT)
GPIO.setup(stepperMotor_PIN2,GPIO.OUT)
GPIO.setup(stepperMotor_PIN3,GPIO.OUT)
GPIO.setup(stepperMotor_PIN4,GPIO.OUT)
#GPIO.setup(error_LED,GPIO.OUT)

#---------Methods----------------------------------------------
#def enable_errorLED():
#    GPIO.output(error_LED,True)

#def disable_errorLED():
#    GPIO.output(error_LED,False)
    
def rotate_clockwise(steps):
    for i in range(0,steps): #ganze Umdrehung
            GPIO.output(stepperMotor_PIN1,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN1,False)
            GPIO.output(stepperMotor_PIN2,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN2,False)
            GPIO.output(stepperMotor_PIN3,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN3,False)
            GPIO.output(stepperMotor_PIN4,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN4,False)

def rotate_counterwise(steps):
    for i in range(0,steps): #ganze Umdrehung
            GPIO.output(stepperMotor_PIN4,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN4,False)
            GPIO.output(stepperMotor_PIN3,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN3,False)
            GPIO.output(stepperMotor_PIN2,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN2,False)
            GPIO.output(stepperMotor_PIN1,True)
            time.sleep(speed)
            GPIO.output(stepperMotor_PIN1,False)
