import RPi.GPIO as GPIO
import time
from rrb2 import *

time.sleep(1.000)

pwmPin = 18
dc = 10
correct = 0.12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 330)
rr = RRB2()

pwm.start(dc)
rr.set_led1(1)

while True:
    dist = rr.get_distance()
    time.sleep(0.5)
    print "Distance is %.2f" % dist

#Straighten motors?
def straightenWheels():
    rr.set_motors(0, 1, 1, 1)
    time.sleep(1.0)
    rr.set_motors(0, 1, 1, 0)
    time.sleep(correct)
    return

def leftTurn(seconds):
    rr.set_motors(1, 1, 1, 1)
    time.sleep(0.3)
    rr.set_motors(1, 1, 0, 1)
    time.sleep(seconds)
    rr.set_motors(1, 1, 1, 0)
    time.sleep(correct)
    return

def rightTurn(seconds):
    rr.set_motors(1, 1, 1, 0)
    time.sleep(0.3)
    rr.set_motors(1, 1, 0, 0)
    time.sleep(seconds)
    rr.set_motors(1, 1, 1, 1)
    time.sleep(correct)
    return

print("Loop, press CTRL C to exit")
straightenWheels()

#Set motors to go
rr.set_motors(1, 1, 0, 1)
time.sleep(3.0)

#Left Turn?
leftTurn(1.5)

#rr.set_motors(1, 1, 0, 1)
#time.sleep(1.0)

#Right Turn?
rightTurn(1.5)

#Slow?
rr.set_motors(1, 1, 0, 1)
time.sleep(3.0)

pwm.stop()
GPIO.cleanup()
