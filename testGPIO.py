import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)

red_ledpin = 21

GPIO.setup(red_ledpin, GPIO.OUT)

GPIO.output(red_ledpin, True)
sleep(5)
GPIO.output(red_ledpin, False)

print('DONE!!')