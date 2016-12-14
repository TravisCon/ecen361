#Libraries
import RPi.GPIO as GPIO
import time

#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 20
GPIO_ECHO = 21

print "Echo Ready"
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

print "Pins Setup"

def _send_trigger_pulse():
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

def _wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(GPIO_ECHO) != value and count > 0:
        count = count - 1

def getDistance():
    _send_trigger_pulse()
    _wait_for_echo(True, 10000)
    start = time.time()
    _wait_for_echo(False, 10000)
    finish = time.time()
    pulse_len = finish - start
    #distance_cm = pulse_len / 0.000058
    distance_cm = (pulse_len * (34300))/2
    return distance_cm


def distance():
	# set Trigger to HIGH
	GPIO.output(GPIO_TRIGGER, True)
	# set Trigger after 0.01ms to LOW
	time.sleep(0.00001)
	print "Pulse Out"
	GPIO.output(GPIO_TRIGGER, False)
	print "Pulse In"

	StartTime = time.time()
	StopTime = time.time()

	# save StartTime
	while GPIO.input(GPIO_ECHO) == 0:
		StartTime = time.time()

	# save time of arrival
	while GPIO.input(GPIO_ECHO) == 1:
		StopTime = time.time()

	# time difference between start and arrival
	TimeElapsed = StopTime - StartTime
	# multiply with the sonic speed (34300 cm/s)
	# and divide by 2, because there and back
	distance = (TimeElapsed * 34300) / 2

	return distance

while True:
	dist = getDistance()
	print "Measured Distance = %.2f cm" % dist
	time.sleep(1)

GPIO.cleanup()
