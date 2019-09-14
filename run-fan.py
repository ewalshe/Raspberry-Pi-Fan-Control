import os
import re
from time import sleep
import signal
import sys
import RPi.GPIO as GPIO

fan_control_gpio_pin = 18
fan_trigger_temperature = 70.0  # The temperature in Celsius above which we trigger the fan
fan_switch_off_temperature = fan_trigger_temperature - 15.0


def initialise_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(fan_control_gpio_pin, GPIO.OUT)
    GPIO.setwarnings(False)
    return


def get_cpu_temperature():
    res = os.popen("vcgencmd measure_temp").readline()
    temp = re.findall("\d+\.\d+", res)[0]
    print("CPU temperature is {0}".format(temp))
    return float(temp)


def set_pin(mode):
    GPIO.output(fan_control_gpio_pin, mode)
    return


def fan_on():
    set_pin(True)
    return


def fan_off():
    set_pin(False)
    return


def check_cpu_temperature_and_activate_fan_if_necessary():
    cpu_temp = get_cpu_temperature()
    if cpu_temp > fan_trigger_temperature:
        fan_on()
    elif cpu_temp < fan_switch_off_temperature:
        fan_off()
    return


try:
    initialise_gpio()
    while True:
        check_cpu_temperature_and_activate_fan_if_necessary()
        sleep(5)
finally:
    GPIO.cleanup()  # resets all GPIO ports used by this program
