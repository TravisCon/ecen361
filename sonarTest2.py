import RPi.GPIO as GPIO
import time

pwmPin = 18
correct = 0.11
TRIGGER_PIN = 18
ECHO_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(pwmPin, GPIO.OUT)
GPIO.setup(TRIGGER_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

def _send_trigger_pulse():
	GPIO.output(TRIGGER_PIN, True)
	time.sleep(0.00001)
	GPIO.output(TRIGGER_PIN, False)

def _wait_for_echo(value, timeout):
	count = timeout
	while GPIO.input(ECHO_PIN) != value and count > 0:
		count = count - 1

def getDistance():
	_send_trigger_pulse()
	_wait_for_echo(True, 10000)
	start = time.time()
	_wait_for_echo(False, 10000)
	finish = time.time()
	pulse_len = finish - start
	#distance_cm = pulse_len / 0.000058
	distance_cm = (pulse_len * (34000))/2
	return distance_cm

def avgDistance():
    list = [2]
    result = 0
    for i in range(0, 2):
        list.append(float(getDistance()))

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
    print "The distance is %.2f cm" % getDistance()
    time.sleep(1)
