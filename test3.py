import RPi.GPIO as GPIO
import time
import random
from rrb2 import *

LED1_PIN = 7
LED2_PIN = 8
pwmPin = 18
correct = 0.11
GPIO_TRIGGER = 20
GPIO_ECHO = 21
GPIO_TRIGGER1 = 19
GPIO_ECHO1= 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 330)

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def _send_trigger_pulse():
	GPIO.output(GPIO_TRIGGER, True)
	time.sleep(0.00001)
	GPIO.output(GPIO_TRIGGER, False)

def _wait_for_echo(value, timeout):
	count = timeout
	while GPIO.input(GPIO_ECHO) != value and count > 0:
		count = count - 1

def getDistanceNew():
	_send_trigger_pulse()
	_wait_for_echo(True, 10000)
	start = time.time()
	_wait_for_echo(False, 10000)
	finish = time.time()
	pulse_len = finish - start
	distance_cm = (pulse_len * (34000))/2
	return distance_cm

# Car Library
class Car:
	correct = 0.12
	speed = 0
	isTurningRight = False
	isTurningLeft = False
	def __init__(self, speed=0):
		self.pwmPin = 18
		self.dc = 10
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.pwmPin, GPIO.OUT)
		self.pwm = GPIO.PWM(self.pwmPin, 330)
		self.rr = RRB2()
		self.pwm.start(self.dc)
		self.rr.set_led1(1)
		#Straighten Wheels
		self.rr.set_motors(0, 1, 1, 1)
		time.sleep(1.0)
		self.rr.set_motors(0, 1, 1, 0)
		time.sleep(self.correct)
		return None
        
	def getDistance(self):
                print "Distance is %.2f" % getDistanceNew()
                return getDistanceNew()
		global temp
                temp = [0, 0, 0]
		for i in range(2):
			temp[i] = getDistanceNew()
			#temp.append(float(self.rr.get_distance()))
		if (temp[0] - temp[1] > 100) or (temp[0] - temp[1] < -100):
			if temp[1] - temp[2] > 100 or temp[1] - temp[2] < -100:
				temp[1] = temp[0]
			else:
				temp[0] = temp[1]
		else:
			if temp[2] - temp[0] > 100 or temp[2] - temp[0] < -100:
				temp[2] = temp[1]
                #print "Distance is %.2f" % float(sum(temp)/len(temp))
                #return float(sum(temp)/len(temp))

	def straighten(self):
		if self.isTurningRight:
			self.rightCorrect()
		if self.isTurningLeft:
			self.leftCorrect()

	def setSpeed(self, speed):
		self.rr.set_led1(0)
		self.rr.set_led2(0)
		self.speed = speed
		self.rr.set_motors(speed,1,0,1)

	def reverse(self):
		self.rr.set_led1(1)
		self.rr.set_led2(1)
		self.rr.set_motors(self.speed, 0, 0,0)

	def leftTurn(self):
		self.rr.set_motors(1, 1, 1, 1)
		time.sleep(0.3)
		self.rr.set_motors(1, 1, 0, 1)
		#time.sleep(seconds)
                self.isTurningLeft = True

	def leftCorrect(self):
		self.rr.set_motors(1, 1, 1, 0)
		time.sleep(self.correct)
                self.isTurningLeft = False

	def rightTurn(self):
		self.rr.set_motors(1, 1, 1, 0)
		time.sleep(0.3)
		self.rr.set_motors(1, 1, 0, 0)
		#time.sleep(seconds)
                self.isTurningRight = True
	def rightCorrect(self):
		self.rr.set_motors(1, 1, 1, 1)
		time.sleep(self.correct)
                self.isTurningLeft = False

car = Car()
car.setSpeed(1.0)

print("Loop, press CTRL C to exit")

#while True:
#	print "Distance is %.2f" % car.getDistance()
#	time.sleep(0.5)

while 1:
	#global car
	dist = car.getDistance()
        time.sleep(0.3)
	#print "Distance is %d" % dist
	if dist > 40.0:
                if dist < 100:
			if random.random() > 0.5:
				car.rightTurn()
			else:
				car.leftTurn()
			while True:
				car.straighten()
				time.sleep(0.01)
				if car.getDistance() > 100:
					break
	else:
		while True:
			car.reverse()
			car.straighten()
			time.sleep(0.3)
			if (car.getDistance() > 40):
				break
		car.setSpeed(1)

print "exit"

pwm.stop()
GPIO.cleanup()
