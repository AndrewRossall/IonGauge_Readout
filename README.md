# IonGauge_Readout
## Short Python script to read and live plot ion gauge data

Python script to liveplot vacuum pressure as read by PGC2 AML Ion Gauge Controller (manufacture 1993).  
AML controller connected using USB serial cable USB to RS232 DB9 9 pin converter cable.  
Script searches for identifier '::::', parses data, extracts reading from IG1 and plots using matplotlib.  

## Installation
Will run as a standalone Python script when AML controller is connected. USB connection set to COM4.  

## Usage
Modules required:  
        matplotlib, numpy, pandas, serial, math, codecs, datetime.  
