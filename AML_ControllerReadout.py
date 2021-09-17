"""
Ion Gauge Readout for AML Controller (via RS232 to USB)

Version 2 and below - Implementing serial connection, import and parse data
Version 2.1 --> 3.4 - Sequential introduction of animated plot
Version 3.5 --> 3.9 - Introduced plot formatting and range control
Version 4.0 - Operational version including date/time stamped output
Version AML_ControllerReadout 
            Basic real time serial read and IG pressure plotting
            Serial flush to prevent buffer overflow
            Data saved in csv
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import random
import serial
import math
import codecs
from datetime import datetime

# initialize serial port
ser = serial.Serial()
ser.port = 'COM4' 
ser.baudrate = 2400     
ser.stopbits = 2
ser.handshake = 'N'
ser.open()

# Write confirmation of serial open and config to term
if ser.is_open == True:
	print("\nSerial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
plt.style.use('grayscale')
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] 
ys = []   

# Set start time
time1 = datetime.now()
ftime = time1.strftime("%d_%m_%Y %H_%M_%S")

fname = "IonGaugeLog %s.csv" %(ftime)

# Open csv file for data record, set-up headings and record start time
with open(fname, 'a') as f:  
        f.write("%s, %s" %(datetime.now().date(), datetime.now().time()))
        f.write('\n')
        f.write("Duration, Pressure (mbar)")
        f.write('\n')

# This function is called from FuncAnimation below at specified interval
def animate(i, xs, ys):    
    
# Aquire and parse data from serial port
    
    data_raw =ser.read(117)                         # Setting for IG controller
    #data_raw =ser.read(119)                        # Setting for Arduino Tester

    # Find marker in serial data
    x = data_raw.find(b'::::')

    # Count from marker to required value
    IGPressure1 = float(data_raw[x+4:x+7])
    IGPressure2 = float(data_raw[x+7:x+10])
    IGPressure = IGPressure1*10**IGPressure2
    IGRed = IGPressure                              # Use this line for any calculations for plot    

    # Calculates duration since start
    time2 = datetime.now()
    difftime = ((time2.hour*60)+time2.minute+(time2.second/60))-((time1.hour*60)+time1.minute+(time1.second/60))

    # Add x and y to lists
    xs.append(difftime)
    ys.append(IGRed)

    # Limit x and y lists to n items - this defines the max range of the x-axis on display
    xs = xs[-600:]
    ys = ys[-600:]

    # Draw x and y lists
    ax.clear()   # This statement required to prevent line stacking
    ax.plot(xs, ys, color="blue") 

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.2, left=0.17)
    plt.title('Storage Chamber Pressure')
    plt.ylabel('Pressure (mbar)')
    plt.semilogy()
    plt.xlabel('Time (mins)')

    # Write data to csv file
    with open(fname, 'a') as f:  
        f.write("%s, %s" %(difftime,IGRed))
        f.write('\n')

    ser.flush()    
   
# Set up plot to call animate() function
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=100)
plt.show()
