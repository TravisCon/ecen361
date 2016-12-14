import RPi.GPIO as GPIO
import time
import random
from rrb2 import *

pwmPin = 18
dc = 10
correct = 0.12
GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 330)
rr = RRB2()
pwm.start(dc)
rr.set_led1(1)

# Car Library
correct = 0.12
speed = 0
def getDistanceSimple():
	return rr.get_distance()
	print "Pre-emptive distance is %d" % rr.get_distance()
        
def getDistance():
	temp = []
	for i in range(2):
		temp.append(float(rr.get_distance()))
	if (temp[0] - temp[1] > 100) or (temp[0] - temp[1] < -100):
		if temp[1] - temp[2] > 100 or temp[1] - temp[2] < -100:
			del temp[1]
		else:
			del temp[0]
	else:
		if temp[2] - temp[0] > 100 or temp[2] - temp[0] < -100:
			del temp[2]
	#print "Pre-emptive distance is %d" % rr.get_distance()
	return float(sum(temp)/len(temp))

def straighten():
	if isTurningRight:
		rightCorrect()
	if isTurningLeft:
		leftCorrect()

def setSpeed(, speed):
	speed = speed
	rr.set_motors(speed,1,0,1)

def reverse():
	rr.set_motors(speed, 0, 0,0)

def leftTurn():
	rr.set_motors(1, 1, 1, 1)
	time.sleep(0.3)
	rr.set_motors(1, 1, 0, 1)

def leftCorrect():
	rr.set_motors(1, 1, 1, 0)
	time.sleep(correct)

def rightTurn():
	rr.set_motors(1, 1, 1, 0)
	time.sleep(0.3)
	rr.set_motors(1, 1, 0, 0)
	#time.sleep(seconds)
	isTurningRight = True

def rightCorrect():
	rr.set_motors(1, 1, 1, 1)
	time.sleep(correct)
 
rr2 = RRB2()
setSpeed(1.0)

print("Loop, press CTRL C to exit")

while 1:
	#global car
	dist = getDistanceSimple()
        time.sleep(0.3)
	print "Distance is %.2f" % rr2.get_distance()
	if dist > 40.0:
                if dist < 100:
			if random.random() > 0.5:
				rightTurn()
			else:
				leftTurn()
			while True:
				straighten()
				time.sleep(0.01)
				if getDistanceSimple() > 100:
					break
	else:
		while True:
			reverse()
			straighten()
			time.sleep(0.3)
			if (getDistanceSimple() > 40):
				break
		setSpeed(1)

print "exit"

pwm.stop()
GPIO.cleanup()
