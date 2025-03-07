#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 10:35:23 2018

@author: tiago
"""

import sys
import matplotlib.pyplot as plt
import numpy as np
import math as mat
import time

# Traemos la libreria VISA
import pyvisa as visa

# Agreamos el path de las librerias
sys.path.insert(0, 'Libreria')
# Traemos la clase base que implmenta las funciones de VISA
from instrument import Instrument


def StartMeasure(instrument, startFreq=100, endFreq=1000, stepSize=200, outVolt=1, dwellTimeMS=1000):

    instrument.write("SOUR:SWE:INT ANAL")           # Sets the sweep generator interface to analog.
    instrument.write("SOUR:FUNC SINE, (@1)")        # Sets the generator waveform type to sine on channel 1.
    amplitudeSet = "SOUR:VOLT " + str(outVolt) + "Vp, (@1)"
    instrument.write(amplitudeSet)                  # Sets the amplitude of the sine waveform to 5 Vp.
    instrument.write("SOUR:SWE:REF:CHAN 1")         # Sets the sweep reference channel of the generator to channel 1.
    instrument.write("SOUR:SWE:CHAN 1")             # Sets channel 1 to perform sweep.
    instrument.write("SOUR:SWE:MODE ASW")           # Sets the sweep mode to Auto.
    instrument.write("SOUR:SWE:PAR FREQ")           # Sets the sweep parameter to frequency.
    instrument.write("SOUR:SWE:SPAC LIN, (@1)")     # Sets the spacing type to linear.
    dwellTime = "SOUR:SWE:DWEL1 " + str(dwellTimeMS)
    instrument.write(dwellTime)                     # Sets the dwell time to dwellTimeMS.
    instrument.write("SENS:MTIM GTR")               # Sets the measurement time to Gen Track.
    sweepStart = "SOUR:SWE:STAR " + str(startFreq)
    instrument.write(sweepStart)                    # Sets the sweep start value to startFreq.
    sweepEnd = "SOUR:SWE:STOP " + str(endFreq)
    instrument.write(sweepEnd)                      # Sets the sweep stop value to endFreq.
    sweepStep = "SOUR:SWE:STEP " + str(stepSize)
    instrument.write(sweepStep)                     # Sets the sweep step size to stepSize.
    instrument.write("SENS:SWE:INT ANAL")           # Sets the sweep analyzer interface to analog.
    instrument.write("SENS:SWE:REF:CHAN 1")         # Sets the sweep reference channel for measurement to channel 1.
    instrument.write("SENS:SWE:CHAN 2")             # Sets the analyzer channel to perform sweep to channel 2.
    instrument.write("SENS:FUNC1 FREQ, (@2)")       # Sets the measurement function 1 to frequency.
    instrument.write("SENS:FUNC2 dBV, (@2)")        # Sets the measurement function 2 to dBV.
    instrument.write("INIT:SWE")                    # Initiates the sweep.
    aux = "1"
    while int(aux) is not 0:                        # Polls the status register to check if the measuring operation
        instrument.write("STAT:OPER:COND?")         # has completed. The condition register will return 0 if the
        time.sleep(5)
        aux = instrument.read()                     # operation has completed.
        print(aux)
        time.sleep(1)
    instrument.write("SOUR:SWE:VAL? (@2)")          # Acquires the X- axis sweep points values.
    xValues = instrument.read_raw()
    instrument.write("FETC:SWE? FUNC1, (@2)")       # Acquires the sweep result for function 1.
    freqValues = instrument.read_raw()
    instrument.write("FETC:SWE? FUNC2, (@2)")       # Acquires the sweep result for function 2
    vacValues = instrument.read_raw()

    xVal = xValues.split(",")
    freqVal = freqValues.split(",")
    vacVal = vacValues.split(",")
    xVal = [float(i) for i in xVal]
    #print(xVal)
    freqVal = [float(i) for i in freqVal]
    #print(freqVal)
    vacVal = [float(i) for i in vacVal]
    #print(vacVal)
    #print(f"type y: {type(vacVal)}")

    return xVal,freqVal,vacVal,1

def AnalyzeFile(instrument, startFreq=100, endFreq=1000, stepSize=200, outVolt=1, dwellTimeMS=1000):

    # Open file and read lines for debugging
    lines = [line.rstrip('\n') for line in open('RAW_Message2')]

    xValues = lines[0]
    freqValues = lines[1]
    vacValues = lines[2]

    xVal = xValues.split(",")
    freqVal = freqValues.split(",")
    vacVal = vacValues.split(",")
    xVal = [float(i) for i in xVal]
    #print(xVal)
    freqVal = [float(i) for i in freqVal]
    #print(freqVal)
    vacVal = [float(i) for i in vacVal]
    #print(vacVal)
    #print(f"type y: {type(vacVal)}")

    return xVal,freqVal,vacVal,1
