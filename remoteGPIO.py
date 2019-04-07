from gpiozero import LED
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

factory = PiGPIOFactory(host='192.168.1.110')
led = LED(26, pin_factory=factory)

led.on()
sleep(5)
led.off()
sleep(1)