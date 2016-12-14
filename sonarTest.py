import RPi.GPIO as GPIO
import time
from rrb2 import *

pwmPin = 18
dc = 10
correct = 0.11
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 320)
rr = RRB2()

def avgDistance():
    list = [2]
    result = 0
    for i in range(0, 2):
        list.append(float(rr.get_distance()))

    if (list[0] - list[1] > 100) or (list[0] - list[1] < -100):
        if list[1] - list[2] > 100 or list[1] - list[2] < -100:
            del list[1]
        else:
            del list[0]
    else:
        if list[2] - list[0] > 100 or list[2] - list[0] < -100:
            del list[2]
            
    result = float(sum(list)/len(list))
    return result
    

while(1):
    distance = avgDistance()
    print "The distance is {} cm".format(distance)
    time.sleep(1)
