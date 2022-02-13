#!/usr/bin/python3

import sys
from easygopigo3 import EasyGoPiGo3
from time import sleep

mybot = EasyGoPiGo3()

#  Set initial values
accumulated_value = 0
count = 0
pause_value = 0.5
reference_input_voltage = 12.00
five_v_system_voltage = 0.00
measured_battery_voltage = 0.00
measured_voltage_differential = 0.00

# file1 = open("./voltage_test.txt", "a")
file1 = open("./voltage_test-"+str(pause_value)+"sec.txt", "a")

def vround(x, decimal_precision=2):

#  vround, ("Vanilla" rounding), always uses "standard" 5/4 rounding and always rounds away from zero regardless of sign.
#
#  "x" is the value to be rounded using "standard" 4/5 rounding rules
#  always rounding away from zero regardless of sign
#
#  "decimal_precision" is the number of decimal places to round to
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


try:
    while True:
        measured_battery_voltage =  vround(mybot.get_voltage_battery(), 3)
        five_v_system_voltage = vround(mybot.get_voltage_5v(), 3)
        measured_voltage_differential =  vround((reference_input_voltage - measured_battery_voltage),3)
        accumulated_value += measured_voltage_differential
        count += 1
        print("Measured Battery Voltage =", measured_battery_voltage)
        print("Measured voltage differential = ", measured_voltage_differential)
        print("5v system voltage =", five_v_system_voltage, "\n")
        print("Total number of measurements so far is ", count)
        sleep(1.00)

except KeyboardInterrupt:
    print("\nThat's All Folks!\n")
    data = ["\nWe took ", str(count), " measurements and the average differential was ", str(vround(accumulated_value/count, 3)), "\n(based on an input reference voltage of ", str(reference_input_voltage), ")\n"]
    file1.writelines(data)
    print("We took ", str(count), " measurements and the average differential was ", str(vround(accumulated_value/count, 3)), "\n(based on an input reference voltage of ", str(reference_input_voltage), ")\n")
    file1.close()
    sys.exit(0)
