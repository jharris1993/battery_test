#!/usr/bin/python3

import sys
from time import sleep

#  This grabs my modified version of EasyGoPiGo3 instead of the standard package
sys.path.insert(0, '/home/pi/Project_Files/Projects/Python_Includes')

from easygopigo3 import EasyGoPiGo3

mybot = EasyGoPiGo3()

#  Set initial values
accumulated_value = 0
count = 0
num_tests_per_cycle = 10  #  Number of tests to run per test cycle
num_test_cyckes = 4
pause_value = 0.50
reference_input_voltage = 12.13
five_v_system_voltage = 0.00
measured_battery_voltage = 0.00
accumulated_voltage = 0.00
average_voltage = 0.00
measured_voltage_differential = 0.00
average_voltage_differential = 0.00

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
    file1 = open("./results/voltage_test-"+str(pause_value)+"sec.txt", "a")
    return (file1)



def write_data(file_handle):
    print("\nThat's All Folks!\n")
    data = [str(count), " measurements were taken every ", str(pause_value), " seconds, and the average voltage differential was ", str(average_voltage_differential), "\n(based on an input reference voltage of ", str(reference_input_voltage), ")\n\n"]
    file_handle.writelines(data)
    print(str(count), " measurements were taken every ", pause_value, " seconds, and the average voltage differential was ", str(average_voltage_differential), "\n(based on an input reference voltage of ", str(reference_input_voltage), ")\n\n")
    file_handle.close()



def run_test():
    global count
    global measured_battery_voltage
    global measured_voltage_differential
    global five_v_system_voltage
    global accumulated_value
    global accumulated_voltage
    global average_voltage
    global average_voltage_differential

    accumulated_value = 0
    accumulated_voltage = 0
    while count < num_tests_per_cycle:
        measured_battery_voltage =  vround(mybot.get_voltage_battery(), 2)
        five_v_system_voltage = vround(mybot.get_voltage_5v(), 2)
        measured_voltage_differential =  vround((reference_input_voltage - measured_battery_voltage),2)
        accumulated_voltage += measured_battery_voltage
        accumulated_value += measured_voltage_differential
        
        count += 1
        # print("Measured Battery Voltage =", measured_battery_voltage)
        # print("Measured voltage differential = ", measured_voltage_differential)
        # print("5v system voltage =", five_v_system_voltage, "\n")
#        print("Total number of measurements so far is ", count)
        sleep(pause_value)
    average_differential = (vround(accumulated_value/count, 2))
    average_voltage = (vround(accumulated_voltage/count, 2))
    return(average_differential)

if __name__ == "__main__":
    print("\nNow starting", num_test_cyckes, "test cycles that will run", num_tests_per_cycle, "times per cycle every", pause_value, "seconds\n")
    x = 0
    cumulative_differential = 0
    cumulative_average = 0
    f = open_file()
    while x < num_test_cyckes:
        try:
#            f = open_file()
            count = 0
            print("Test Cycle ", str(x+1), " of ", str(num_test_cyckes), " which consists of ", str(num_tests_per_cycle), " tests every ", str(pause_value), " seconds)")
            data = ["Test Cycle ", str(x+1), " of ", str(num_test_cyckes), " which consists of ", str(num_tests_per_cycle), " tests every ", str(pause_value), " seconds)\n"]
            f.writelines(data)
            average_voltage_differential = 0.00
            average_voltage_differential = run_test()
            print("The Average Differential for this test cycle was ", str(average_voltage_differential), "volts\n")
            print("The average voltage for this test cycle was ", str(average_voltage), "volts\n")
            data = ["The Average Differential for this test cycle was ", str(average_voltage_differential), "\n\n"]
            f.writelines(data)
            data = ["The Average voltage for this test cycle was ", str(average_voltage), "\n\n"]
            f.writelines(data)
            cumulative_differential += average_voltage_differential

        except KeyboardInterrupt:
            # file1 = open("./voltage_test.txt", "a")
            print("keyboard exception")
            write_data(f)
            sys.exit(0)
        else:
            x += 1

    cumulative_average = (vround(cumulative_differential/x, 2))
    print("The cumulative average of all the test cycles was ", str(cumulative_average), "\n")
#    f = open_file()
    data = ["===================================\nThe cumulative average of all the test cycles was ", str(cumulative_average), "\n===================================\n\n"]
    f.writelines(data)
    f.close()
