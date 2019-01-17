import serial
import time
import csv
import threading
from serial import SerialException
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

parsedInDecimal = 0
values = []
lastMovementDirection = "Stay"
comConnection = False
com_port = '0'

# this will store the line
seq = []
count = 1

def callback(self):
    self.root.quit()

def updateTempLabel(self, value):
    self.root.label_temp.config(text="Temp: " + str(value))

def updateLightLabel(self, value):
    self.root.label_light.config(text="Light: " + str(value))

def startButtonPressed():
    print("Start Button Pressed")
    ser.write("1".encode())

def stopButtonPressed():
    print("Stop button Pressed")
    ser.write("2".encode())

def runWholeThing():
    count = 1

    print("Into Thread")

    while True:

        print("into True")

        if comConnection:
            print("Into Com Connection")
            if ser.inWaiting() > 0 and comConnection:
                print("Into ser waiting")
                for c in ser.read():
                    seq.append(chr(c))  # convert from ANSII
                    joined_seq = ''.join(str(v) for v in seq)  # Make a string from array

                    print(joined_seq)

                    if chr(c) == '\n':
                        print("Line " + str(count) + ': ')
                        seq = []
                        count += 1

                        parsedBeginningLetter = joined_seq[0]
                        parsedContent = joined_seq[6:9]
                        print(parsedBeginningLetter)
                        print("Hex: " + parsedContent)

                        if parsedContent and parsedContent.strip():
                            parsedInDecimal = int(parsedContent, 16)
                            print("Decimal: " + str(parsedInDecimal))
                            values.append(parsedInDecimal)
                            values.pop(0)

                            calculatedOn = (5000 / 4096) * parsedInDecimal

                        if parsedBeginningLetter == "A":
                            calculatedOn = (5000 / 4096) * parsedInDecimal
                            print("Millivolt Value :" + str(calculatedOn))

                            temperatureCalculated = (calculatedOn - 2103) / -10.9
                            print("Temperature: " + str(temperatureCalculated))

                            updateTempLabel(temperatureCalculated)
                            # app.refreshTemperatureGraph(temperatureCalculated)
                            # app.createTemperaturegraph()
                            # app.createSecondLightgraph()

                            if lastMovementDirection == "Up":
                                with open("C:/Temp/test_data_Temp.csv", "a") as f:
                                    writer = csv.writer(f, delimiter=",")
                                    writer.writerow([time.time(), count, parsedBeginningLetter, calculatedOn, "0",
                                                     temperatureCalculated])
                            elif lastMovementDirection == "Down":
                                with open("C:/Temp/test_data_Temp.csv", "a") as f:
                                    writer = csv.writer(f, delimiter=",")
                                    writer.writerow(
                                        [time.time(), count, parsedBeginningLetter, calculatedOn,
                                         temperatureCalculated,
                                         "0"])
                            else:
                                print("Boooo0o0")

                        if parsedBeginningLetter == "B":

                            updateLightLabel(parsedInDecimal)

                            if lastMovementDirection == "Up":
                                with open("C:/Temp/test_data_Light.csv", "a") as f:
                                    writer = csv.writer(f, delimiter=",")
                                    writer.writerow(
                                        [time.time(), count, parsedBeginningLetter, "0", parsedInDecimal])
                            elif lastMovementDirection == "Down":
                                with open("C:/Temp/test_data_Light.csv", "a") as f:
                                    writer = csv.writer(f, delimiter=",")
                                    writer.writerow(
                                        [time.time(), count, parsedBeginningLetter, parsedInDecimal, "0"])

                        if parsedBeginningLetter == "C":
                            scaledDecimalE = parsedInDecimal - 500

                            print("Error Act: ", scaledDecimalE)

                            with open("C:/Temp/test_data_Error.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, scaledDecimalE])

                        if parsedBeginningLetter == "D":
                            scaledDecimalI = parsedInDecimal - 500

                            print("Integral Act: ", scaledDecimalI)

                            with open("C:/Temp/test_data_Integral.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, scaledDecimalI])

                        if parsedBeginningLetter == "E":
                            scaledDecimalD = parsedInDecimal - 500

                            print("Derivitive Act: ", scaledDecimalD)

                            print("\nE: " + str(scaledDecimalE))
                            print("I: " + str(scaledDecimalI))
                            print("D: " + str(scaledDecimalD))

                            # Local Calc for control Variable
                            controlVariable = scaledDecimalE * 0.02 + scaledDecimalI * 0.00 + scaledDecimalD * 4.0
                            print("Control Var: ", controlVariable)

                            with open("C:/Temp/test_data_ControlVar.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, "Cont", controlVariable])

                            with open("C:/Temp/test_data_Derivative.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, scaledDecimalD])

                        if parsedBeginningLetter == "U":
                            print("Up")
                            lastMovementDirection = "Up"

                        if parsedBeginningLetter == "Z":
                            print("Down")
                            lastMovementDirection = "Down"

                        if parsedBeginningLetter == "M":
                            print("Stay")
                            lastMovementDirection = "Stay"

                        print("\n")
                        break

def connectToCOM():
    try:
        global ser
        global comConnection

        #temp = 'COM' + com_port.rstrip()
        temp = 'COM3'
        print('Connect from 3')

        ser = serial.Serial(
            port=temp, \
            baudrate=9600, \
            parity=serial.PARITY_NONE, \
            stopbits=serial.STOPBITS_ONE, \
            bytesize=serial.EIGHTBITS, \
            timeout=0)

        comConnection = True
        print("connected to: " + ser.portstr)

        threading.Thread(target=runWholeThing()).start()
        print("After Thread")

        #runWholeThing()

    except SerialException:
        print("Port Issue: ")
        ser = None

        comConnection = False


root = tk.Tk()
root.protocol("WM_DELETE_WINDOW", callback)
root.x_count = 1




def create_buttons(root):
    root.title("Vanuatu GUI")
    root.geometry("1000x550")
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.button_frame = tk.Frame()
    root.btn_start = tk.Button(text="Start", command=startButtonPressed)
    root.btn_stop = tk.Button(text="Stop", command=stopButtonPressed)
    root.label_temp = tk.Label(text="Temp:")
    root.label_light = tk.Label(text="Light:")
    root.setting_button = tk.Button(text="Settings")
    root.connect_button = tk.Button(text="Connect", command=connectToCOM)
    root.connect_button.grid(row=1, column=1)
    root.setting_button.grid(row=1, column=0)
    root.label_light.grid(row=3, column=1)
    root.label_temp.grid(row=3, column=0)
    root.btn_start.grid(row=2, column=0)
    root.btn_stop.grid(row=2, column=1)

create_buttons(root)
#app = App()
print(comConnection)
root.mainloop()


#root.update_idletasks()
#root.update()

# Change Order here, and put while true a few steps down after com is confirmed


#ser.close()


