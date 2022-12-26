import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import asyncio
import time
import threading
import json
import math
import numpy as np


# Connect to UART
ser = serial.Serial('COM37', baudrate = 115200, timeout=1)

def getDataPowerStart():
    while True:
        message = ser.read()

        if message == b'\xa5':
            nxRead = ser.read(1)

            if nxRead == b'Z':
                # Get Data Length
                bufLength = ser.read(4)
                length = int.from_bytes(bufLength, 'little')
                print("Length data : %d" %length)

                # Get Response Mode
                mode = int.from_bytes(bufLength[:1], 'little')
                if mode == 20:

                    print("Mode Response : single")

                # Get Model
                model = ser.read(1)
                if model == b'\x04':
                    print('Model : X2')

                # Get Low Firmware Version
                bufLowFirmware = ser.read(1)
                lowFirmware = int.from_bytes(bufLowFirmware, 'little')

                # Get High Firmware Version
                bufHighFirmware = ser.read(1)
                highFirmware = int.from_bytes(bufHighFirmware, 'little')
                print('Software Version : V%d.%d'%(lowFirmware,highFirmware))       

                # Get Hardware Version
                bufHardwareVer = ser.read(1)
                hardwareVer = int.from_bytes(bufHardwareVer, 'little')
                print("Hardware version : V%d" %hardwareVer)

                # Get Serial Number
                bufSerialNumber = ser.read(16)
                serialNumber = int.from_bytes(bufSerialNumber, 'little')
                print("Serial Number : %x" %serialNumber)
                print('*'*50)
                break

def getDataStartUp():
    while True:
        message = ser.read()

        if message == b'\xa5':
            nextMes = ser.read(1)
            if nextMes == b'Z':

                # Get Data Length
                bufLength = ser.read(4)
                length = int.from_bytes(bufLength, 'little')
                print("Length data : %d" %length)

                # Get Response Mode
                mode = int.from_bytes(bufLength[:1], 'little')
                if mode == 5:
                    print("Mode Response : continous")
                

                # Get Type Code
                buf = ser.read(1)
                typeData = int.from_bytes(buf, 'little')
                print("Type data : %d" %typeData)
                print('*'*50)
                break

Xraw = []
Yraw = []
def scanning():

    dataStreamDistance = []
    dataStreamAngle = []
    dataAngleToDistance = np.zeros(361)
    while True:
        message = ser.read()
        
        # Find the Header
        if message == b'\xaa':
            nexMes = ser.read(1)
            if nexMes == b'U':

                # Get Current Type of package
                buf = ser.read(1)
                CT = int.from_bytes(buf, 'little')
                print("Type Data : %d" %CT)
                
                # Get Sample Quantity
                buf = ser.read(1)
                LSN = int.from_bytes(buf, 'little')
                print("Number of Sample : %d" %LSN)

                # Get Starting Point Angle
                buf = ser.read(2)
                FSA = int.from_bytes(buf, 'little')
                AngleStart = (FSA >> 1)/64
                print("Start Angle : %.2f" %AngleStart)

                # Get End Point Angle
                buf = ser.read(2)
                LSA = int.from_bytes(buf, 'little')
                AngleEnd = (LSA >> 1)/64
                print("End Angle : %.2f" %AngleEnd)

                # Get Check Sum Code
                buf = ser.read(2)
                CS = int.from_bytes(buf, 'little')
                print("Check Sum : %d" %CS)

                for i in range(LSN):
                    # Get Distance
                    buf = ser.read(2)
                    S = int.from_bytes(buf, 'little')
                    Distance = S/4

                    # Get Angle at I
                    if i == 0:
                        A = AngleStart
                    elif i == (LSN-1):
                        A = AngleEnd
                    else:
                        A = (((AngleEnd-AngleStart)/(LSN-1))*((i+1)-1))+AngleStart
                    
                    # Get Angle Correction
                    if Distance == 0:
                        Ar = 0
                    else :
                        Ar = math.atan2(21.8*(155.3-Distance),(155.3*Distance))

                    trueAngle = A + Ar
                    Angle = int(round(trueAngle))

                    if Distance != 0 and Angle <= 360:
                        
                        dataStreamDistance.append(Distance)
                        dataStreamAngle.append(Angle)
                        dataAngleToDistance[Angle] = Distance
                        

                    # print("Data%d : %.2f"%((i+1),Distance)+" - %.2f"%trueAngle)
                # print('*'*150)

                    for i in range(0,360):
                        if dataAngleToDistance[i] > 1 and dataAngleToDistance[i] < 1000:
                            Xraw.append((math.cos(math.radians(i)))*dataAngleToDistance[i])
                            Yraw.append((math.sin(math.radians(i)))*dataAngleToDistance[i])

                    dataStr = np.array_str(dataAngleToDistance)
                    with open("data.txt", "w") as file:
                    # write an empty string to the file
                        file.write(dataStr)
                    file.close()
                    # plt.clf()
                    # plt.scatter(Xraw, Yraw, s=100, c="Green", linewidth=0.1, alpha=0.5)  
                    # plt.title("Lidar Scanning")  
        
        


scanning()
  
