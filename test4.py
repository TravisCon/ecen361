import RPi.GPIO as GPIO
import time
import random
from rrb2 import *

temp = [0, 0, 0]
pwmPin = 18
correct = 0.11
GPIO_TRIGGER0 = 20
GPIO_ECHO0 = 21
GPIO_TRIGGER1 = 19
GPIO_ECHO1 = 26

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
pwm = GPIO.PWM(pwmPin, 330)

GPIO.setup(GPIO_TRIGGER0, GPIO.OUT)
GPIO.setup(GPIO_ECHO0, GPIO.IN)
GPIO.setup(GPIO_TRIGGER1, GPIO.OUT)
GPIO.setup(GPIO_ECHO1, GPIO.IN)

def _send_trigger_pulse(trigger):
	GPIO.output(trigger, True)
	time.sleep(0.00001)
	GPIO.output(trigger, False)

def _wait_for_echo(echo, value, timeout):
	count = timeout
	while GPIO.input(echo) != value and count > 0:
		count = count - 1

def getDistanceNew(echo, trigger):
	_send_trigger_pulse(trigger)
	_wait_for_echo(echo, True, 10000)
	start = time.time()
	_wait_for_echo(echo, False, 10000)
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
		distLeft = getDistanceNew(GPIO_ECHO0, GPIO_TRIGGER0)
		distRight = getDistanceNew(GPIO_ECHO1, GPIO_TRIGGER1)

		print "Distance is |%10.2f | %10.2f| " % (distLeft, distRight)
		return min(distLeft, distRight), distLeft, distRight
		#print "Distance is %.2f" % float(sum(temp)/len(temp))
		#return float(sum(temp)/len(temp))

	def straighten(self):
		if self.isTurningRight:
			self.isTurningRight = False
			self.rightCorrect()
		if self.isTurningLeft:
			self.isTurningLeft = False
			self.leftCorrect()

	def setSpeed(self, speed):
		self.rr.set_led1(0)
		self.rr.set_led2(0)
		self.speed = speed
		self.rr.set_motors(speed, 1, 0, 1)

	def reverse(self):
		print "				REVERSE"
		self.rr.set_led1(1)
		self.rr.set_led2(1)
		self.rr.stop()
		time.sleep(0.05)
		self.rr.set_motors(1, 0, 0, 0)

	def leftTurn(self):
		if self.isTurningRight == True:
			return
		self.rr.set_motors(1, 1, 1, 1)
		time.sleep(0.3)
		self.rr.set_motors(1, 1, 0, 1)
		#time.sleep(seconds)
		self.isTurningLeft = True
		self.isTurningRight = False

	def leftCorrect(self):
		self.rr.set_motors(1, 1, 1, 0)
		time.sleep(self.correct)
		self.isTurningLeft = False

	def rightTurn(self):
		if self.isTurningLeft == True:
			return
		self.rr.set_motors(1, 1, 1, 0)
		time.sleep(0.3)
		self.rr.set_motors(1, 1, 0, 0)
		self.isTurningRight = True
		self.isTurningLeft = False
        #time.sleep(seconds)

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
	dist, ld, rd = car.getDistance()
	time.sleep(0.3)
	#print "Distance is %d" % dist

	if dist > 60.0:
		print "Greater than 40cm"
		if dist < 175:
			#print "Less than 100cm"
			#if random.random() > 0.5:
			if dist == ld:
				car.rightTurn()
				time.sleep(0.4)
			else:
				car.leftTurn()
				time.sleep(0.4)
			time.sleep(0.01)
		else:
			car.straighten()

	else:
		print "   Entering WHILE"
		#car.rr.set_motors(1, 0, 0, 0)
		car.straighten()
		car.reverse()
		while True:
			time.sleep(0.4)
			if (car.getDistance()[0] > 60):
				break
		print "   Exited Reverse"
		car.setSpeed(1)

print "exit"

pwm.stop()
GPIO.cleanup()
