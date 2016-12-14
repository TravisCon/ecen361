import RPi.GPIO as GPIO
import time
from rrb2 import *

time.sleep(1.000)

pwmPin = 18
dc = 10
correct = 0.11
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 320)
rr = RRB2()

pwm.start(dc)
rr.set_led1(1)

#Straighten motors?
def straightenWheels():
    rr.set_motors(0, 1, 1, 1)
    time.sleep(1.0)
    rr.set_motors(0, 1, 1, 0)
    time.sleep(correct)
    return

def rightTurn(seconds):
    rr.set_motors(1, 1, 1, 1)
    time.sleep(seconds)
    rr.set_motors(1, 1, 1, 0)
    time.sleep(correct)
    return

def leftTurn(seconds):
    rr.set_motors(1, 1, 1, 0)
    time.sleep(seconds)
    rr.set_motors(1, 1, 1, 1)
    time.sleep(correct)
    return

straightenWheels()

#Set motors to go
rr.set_motors(1, 1, 0, 1)
time.sleep(3.0)
print("Loop, press CTRL C to exit :)")

#Left Turn?
leftTurn(2.5)

#Right Turn?
rightTurn(2.0)

#Slow?
rr.set_motors(0.5, 1, 0, 1)
time.sleep(3.0)

pwm.stop()
GPIO.cleanup()
