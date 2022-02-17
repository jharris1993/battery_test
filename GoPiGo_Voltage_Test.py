#!/usr/bin/python3

import sys
from time import sleep

#  This grabs my modified version of EasyGoPiGo3 instead of the standard package
sys.path.insert(0, '/home/pi/Project_Files/Projects/Python_Includes')

from easygopigo3 import EasyGoPiGo3

mybot = EasyGoPiGo3()

#  Set initial values
count = 0
num_tests_per_cycle = 10  #  Number of tests to run per test cycle
num_test_cyckes = 4
pause_value = 0.35
decimal_precision = 2
measured_5v = 0.00
measured_battery_voltage = 0.00
battery_voltage_sum = 0.00
five_v_sum = 0.00
average_battery_voltage = 0.00
average_5v = 0.00
cumulative_5v_average = 0.00
cumulative_battery_average = 0.00

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

def open_file():
    # file1 = open("./voltage_test.txt", "a")
#    file1 = open(".results/GoPiGo_Voltage_test/GoPiGo_Voltage_test-"+str(pause_value)+"sec.txt", "a")    return (file1)
    file1 = open("./results/voltage_test-"+str(pause_value)+"sec.txt", "a")
    return(file1)


def write_data(file_handle):
    print("\nThat's All Folks!\n")
    data = [str(count), " measurements were taken every ", str(pause_value), " seconds.\n The average battery voltage was ", str(average_battery_voltage), "\nThe average 5v VCC rail was ", str(average_5v), ")\n\n"]
    file_handle.writelines(data)
    print(str(count), " measurements were taken every ", str(pause_value), " seconds.\n The average battery voltage was ", str(average_battery_voltage), "\nThe average 5v VCC rail was ", str(average_5v), ")\n\n")
    file_handle.close()



def run_test():
    global count
    global measured_battery_voltage
    global measured_5v
    global five_v_sum
    global battery_voltage_sum
    global average_battery_voltage
    global average_5v
    global cumulative_5v_average
    global cumulative_battery_average

    battery_voltage_sum = 0
    five_v_sum = 0
    while count < num_tests_per_cycle:
        measured_battery_voltage =  vround(mybot.get_voltage_battery(), decimal_precision)
        measured_5v = vround(mybot.get_voltage_5v(), decimal_precision)
        battery_voltage_sum += measured_battery_voltage
        five_v_sum += measured_5v
        count += 1
        sleep(pause_value)
    average_5v = (vround(five_v_sum/count, decimal_precision))
    average_battery_voltage = (vround(battery_voltage_sum/count, decimal_precision))
    return()

if __name__ == "__main__":
    print("\nNow starting", num_test_cyckes, "test cycles that will run", num_tests_per_cycle, "times per cycle every", pause_value, "seconds\n")
    x = 0
    f = open_file()
    while x < num_test_cyckes:
        try:
#            f = open_file()
            count = 0
            print("Test Cycle ", str(x+1), " of ", str(num_test_cyckes), " which consists of ", str(num_tests_per_cycle), " tests every ", str(pause_value), " seconds")
            data = ["Test Cycle ", str(x+1), " of ", str(num_test_cyckes), " which consists of ", str(num_tests_per_cycle), " tests every ", str(pause_value), " seconds\n"]
            f.writelines(data)
            average_5v = 0.00
            average_battery_voltage = 0.00
            run_test()
            print("The average battery voltage for this test cycle was ", str(average_battery_voltage), "volts")
            print("The average 5v VCC voltage for this test cycle was ", str(average_5v), "volts\n")
            data = ["The average battery voltage for this test cycle was ", str(average_battery_voltage), "volts\n"]
            f.writelines(data)
            data = ["The average 5v VCC voltage for this test cycle was ", str(average_5v), "volts\n\n"]
            f.writelines(data)
            cumulative_5v_average += average_5v
            cumulative_battery_average += average_battery_voltage

        except KeyboardInterrupt:
            # file1 = open("./voltage_test.txt", "a")
            print("keyboard exception")
            write_data(f)
            sys.exit(0)
        else:
            x += 1

    print("===================================\nThe 5v average of all the test cycles was ", str((vround(cumulative_5v_average/x))))
    print("The battery voltage average of all the test cycles was ", str((vround(cumulative_battery_average/x))), "\n===================================\n\n") 
#    f = open_file()
    data = ["===================================\n"]
    f.writelines(data)
    data = ["The 5v average of all the test cycles was ", str((vround(cumulative_5v_average/x))), "\n"]
    f.writelines(data)
    data = ["The battery voltage average of all the test cycles was ", str((vround(cumulative_battery_average/x))), "\n"]
    f.writelines(data)
    data = ["===================================\n"]
    f.writelines(data)
    f.close()
