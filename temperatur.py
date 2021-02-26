from time import sleep
import RPi.GPIO as GPIO
import os
import glob

os.system('modprobe w1-gpio')                                                                                                                                                                                                                os.system('modprobe w1-therm')
GPIO.setmode(GPIO.BCM)
RELAIS_PIN = 17
GPIO.setup(RELAIS_PIN, GPIO.OUT)
#GPIO.output(RELAIS_PIN, GPIO.LOW)

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()                                                                                                                                                                                                                  equals_pos = lines[1].find('t=')                                                                                                                                                                                                             if equals_pos != -1:                                                                                                                                                                                                                             temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c

try:
        while True:
            i=(read_temp())
            if i >= 21.000:
                GPIO.output(RELAIS_PIN, True)
                print(i,'°C >> True')
                sleep(2)
            else:
                GPIO.cleanup()
                GPIO.setmode(GPIO.BCM)
                RELAIS_PIN = 17
                GPIO.setup(RELAIS_PIN, GPIO.OUT)
                #GPIO.cleanup()
                #GPIO.output(RELAIS_PIN, False)
                print(i,'°C >> False')
                sleep(2)

except KeyboardInterrupt:
        GPIO.output(RELAIS_PIN, False)
        GPIO.cleanup()
        print("power off fan...")
        #GPIO.output(RELAIS_PIN, False)
