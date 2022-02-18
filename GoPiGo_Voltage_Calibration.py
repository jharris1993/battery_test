#!/usr/bin/python3

import sys
from time import sleep

#  This grabs my modified version of EasyGoPiGo3 instead of the standard package
sys.path.insert(0, '/home/pi/Project_Files/Projects/Python_Includes')

from easygopigo3 import EasyGoPiGo3

mybot = EasyGoPiGo3()

#  Set parametric values
pause_value = 0.25  #  How long to wait between individual tests per cycle
decimal_precision = 2  #  The degree of decimal precision to report (anythng greater than 2 will show a lot of noise)

def vround(x, decimal_precision=2):

#  vround, ("Vanilla" rounding), always uses "standard" 5/4 rounding and always rounds away from zero regardless of sign.
#
#  "x" is the value to be rounded using "standard" 4/5 rounding rules
#  always rounding away from zero regardless of sign
#
#  "decimal_precision" is the number of decimal places to round to which defaults to 2 if not specified.
#
    if decimal_precision < 0:
        decimal_precision = 0

    exp = 10 ** decimal_precision
    x = exp * x

    if x > 0:
        val = (int(x + 0.5) / exp)
    elif x < 0:
        val = (int(x - 0.5) / exp)
    else:
        val = 0
        
    if decimal_precision <= 0:
        return (int(val))
    else:
        return (val)

def run_test():
    global pause_value
    global decimal_precision

    while True:
        measured_battery =  vround(mybot.get_voltage_battery(), decimal_precision)
        measured_vcc = vround(mybot.get_voltage_vcc(), decimal_precision)
        measured_5v = vround(mybot.get_voltage_5v(), decimal_precision)
        print("Battery Voltage =", measured_battery, "volts")
        print("VCC voltage =", measured_vcc, "volts")
        print("5v Raspberry Pi voltage =", measured_5v, "volts")
        sleep(pause_value)
    return()

if __name__ == "__main__":
    try:
        run_test()

    except KeyboardInterrupt:
        print("\nShutdown")
        sys.exit(0)
