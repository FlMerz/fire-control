'''
Created on 13.01.2014

@author: Stefan

based on Matt Hawkins tutorial: http://www.raspberrypi-spy.co.uk/2012/07/stepper-motor-control-in-python/

Usage:
    import StepperControl.stepper
    import time
    
    # initialize GPIO24,GPIO25,GPIO8,GPIO7
    stepper = StepperControl.stepper.Stepper(24,25,8,7)
    # number of steps
    steps = 165

    while True:
       stepper.rotate_clockwise(steps)
       time.sleep(5)
       stepper.rotate_counterwise(steps)

'''

import time
import RPi.GPIO as GPIO


class Stepper:

    def __init__(self, pin1,pin2,pin3,pin4):
        GPIO.setmode(GPIO.BCM)
        self.StepPins = [pin1,pin2,pin3,pin4]
        # Set all pins as output
        for pin in self.StepPins:
            GPIO.setup(pin,GPIO.OUT)
            GPIO.output(pin, False)
        # Define some settings
        self.WaitTime = 0.1
        
        # Define simple sequence
        self.StepCount1 = 4
        self.Seq1 = []
        self.Seq1 = range(0, self.StepCount1)
        self.Seq1[0] = [1,0,0,0]
        self.Seq1[1] = [0,1,0,0]
        self.Seq1[2] = [0,0,1,0]
        self.Seq1[3] = [0,0,0,1]
        
        # Define advanced sequence
        # as shown in manufacturers datasheet
        self.StepCount2 = 8
        self.Seq2 = []
        self.Seq2 = range(0, self.StepCount2)
        self.Seq2[0] = [1,0,0,0]
        self.Seq2[1] = [1,1,0,0]
        self.Seq2[2] = [0,1,0,0]
        self.Seq2[3] = [0,1,1,0]
        self.Seq2[4] = [0,0,1,0]
        self.Seq2[5] = [0,0,1,1]
        self.Seq2[6] = [0,0,0,1]
        self.Seq2[7] = [1,0,0,1]
        
        # Choose a sequence to use
        self.Seq = self.Seq2
        self.StepCount = self.StepCount2

    def rotate_clockwise(self,steps):
        StepCounter = 0
        while steps > 0:
                for pin in range(0, 4):
                    xpin = self.StepPins[pin]
                    if self.Seq[StepCounter][pin]!=0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
        
                StepCounter += 1
                if (StepCounter==self.StepCount):
                    StepCounter = 0
                if (StepCounter<0):
                    StepCounter = self.StepCount
        
                time.sleep(self.WaitTime)
                steps -= 1
        self.reset_pins()

    def rotate_counterwise(self,steps):
        StepCounter = self.StepCount - 1
        while steps > 0:
                for pin in range(0, 4):
                    xpin = self.StepPins[pin]
                    if self.Seq[StepCounter][pin]!=0:
                        GPIO.output(xpin, True)
                    else:
                        GPIO.output(xpin, False)
        
                StepCounter -= 1
                if (StepCounter <= 0):
                    StepCounter = self.StepCount - 1
        
                time.sleep(self.WaitTime)
                steps -= 1
        self.reset_pins()
                
    def reset_pins(self):
        for pin in self.StepPins:
            GPIO.output(pin, False)

