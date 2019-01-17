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


def readInSettings():
    print("Settings")

    with open("C:/Temp/app_settings.txt") as f:
        lines = f.readlines()
        print(lines)

        print(lines[0])

        global com_port

        com_port = lines[0]


def doAtExit():
    ser.close()
    print("Close serial")
    print("serialArduino.isOpen() = " + str(ser.isOpen()))


#atexit.register(doAtExit)
# this will store the line
seq = []
count = 1


# pre-load dummy data
for i in range(0, 26):
    values.append(0)


class PopupWindow(object):
    def __init__(self, master):
        self.top = tk.Toplevel()
        self.entry = tk.Entry(self.top)
        self.entry.grid(row=1, column=1)
        self.top.com_confirm = tk.Button(self.top, text="Okay", command=self.take_COM_value)
        self.top.com_confirm.grid(row=1, column=2)
        self.comLabel = tk.Label(self.top, text="COM #")
        self.comLabel.grid(row=1, column=0)
        self.entry.insert(0, com_port)

    def take_COM_value(self):
        print("Take Com Value")
        print(self.entry.get())

        with open("C:/Temp/app_settings.txt", "a") as p:
            settingsWriter = csv.writer(p, delimiter=",")
            settingsWriter.writerow([self.entry.get()])


class App(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        readInSettings()

    def callback(self):
        self.root.quit()

    def create_buttons(self):
        self.root.title("Vanuatu GUI")
        self.root.geometry("1000x550")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.button_frame = tk.Frame()
        self.root.btn_start = tk.Button(text="Start", command=self.startButtonPressed)
        self.root.btn_stop = tk.Button(text="Stop", command=self.stopButtonPressed)
        self.root.label_temp = tk.Label(text="Temp:")
        self.root.label_light = tk.Label(text="Light:")
        self.root.setting_button = tk.Button(text="Settings", command=self.settingsWindowOpen)
        self.root.connect_button = tk.Button(text="Connect", command=self.connectToCOM)

        self.root.connect_button.grid(row=1, column=1)
        self.root.setting_button.grid(row=1, column=0)
        self.root.label_light.grid(row=3, column=1)
        self.root.label_temp.grid(row=3, column=0)
        self.root.btn_start.grid(row=2, column=0)
        self.root.btn_stop.grid(row=2, column=1)

    def createTemperaturegraph(self):
        self.root.temperature_f = Figure(figsize=(5, 5), dpi=100)
        self.root.ax = self.root.temperature_f.add_subplot(111)
        self.root.temperature_x = [0,1,2]
        self.root.temperature_y = [0,1,3]
        self.root.temperature_x_count = 3
        self.root.temperature_line = self.root.ax.plot(self.root.temperature_x, self.root.temperature_y)
        self.root.temperature_canvas = FigureCanvasTkAgg(self.root.temperature_f, self.root)
        self.root.temperature_f.suptitle("Temperature Graph")

        self.root.temperature_canvas.draw()
        self.root.temperature_canvas.get_tk_widget().grid(row=4, column=0)

    def createLightgraph(self):
        self.root.f = Figure(figsize=(5,5), dpi=100)
        self.root.lightGraph = self.root.f.add_subplot(111)
        self.root.x = []
        self.root.y = []
        self.root.x_count = 0
        self.root.line = self.root.lightGraph.plot(self.root.x,self.root.y)
        self.root.canvas = FigureCanvasTkAgg(self.root.f, self.root)
        self.root.f.suptitle("Light Graph")
        self.root.canvas.draw()
        self.root.canvas.get_tk_widget().grid(row=4, column=1)

    def createSecondLightgraph(self):
        self.root.figtwo = Figure(figsize=(5,5), dpi=100)
        self.root.lightGraphtwo = self.root.figtwo.add_subplot(111)
        self.root.xtwo = [10,11,12,13,14]
        self.root.ytwo = [10,11,12,13,14]
        self.root.x_counttwo = 5
        self.root.linetwo = self.root.lightGraphtwo.plot(self.root.xtwo,self.root.ytwo)
        self.root.canvastwo = FigureCanvasTkAgg(self.root.figtwo, self.root)
        self.root.figtwo.suptitle("two two Two")
        self.root.canvastwo.draw()

        self.root.canvastwo.get_tk_widget().grid(row=4, column=0)

    def refreshTemperatureGraph(self, value):
        self.root.temperature_x.append(self.root.temperature_x_count)
        self.root.temperature_y.append(value)
        self.root.ax.plot(self.root.temperature_x, self.root.temperature_y)
        self.root.temperature_x_count += 1
        print("GRAPH: Adding Count: ")
        print("GRAPH: Adding Value: " + str(value))

        #self.root.temperature_canvas.draw()
        self.root.label_temp.grid(row=3, column=0)

    def updateTempLabel(self, value):
        self.root.label_temp.config(text="Temp: " + str(value))

    def updateLightLabel(self, value):
        self.root.label_light.config(text="Light: " + str(value))

    def startButtonPressed(self):
        print("Start Button Pressed")
        ser.write("1".encode())

    def stopButtonPressed(self):
        print("Stop button Pressed")
        ser.write("2".encode())

    def settingsWindowOpen(self):
        temp = PopupWindow(self)

    def connectToCOM(self):
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

        except SerialException:
            print("Port Issue: ")
            ser = None

            comConnection = False

    def run(self):
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.callback)

        self.create_buttons()
        self.createTemperaturegraph()
        self.createLightgraph()
        #self.createSecondLightgraph()


        self.root.x_count = 1
        self.root.mainloop()

app = App()
print(comConnection)

# Change Order here, and put while true a few steps down after com is confirmed

while True:

    if comConnection:
        if ser.inWaiting() > 0 and comConnection:
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



                        print("Temperature: " + str(temperatureCalculated))

                        app.updateTempLabel(temperatureCalculated)
                        #app.refreshTemperatureGraph(temperatureCalculated)
                        #app.createTemperaturegraph()
                        #app.createSecondLightgraph()

                        if lastMovementDirection == "Up":
                            with open("C:/Temp/test_data_Temp.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, calculatedOn, "0", temperatureCalculated])
                        elif lastMovementDirection == "Down":
                            with open("C:/Temp/test_data_Temp.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, calculatedOn, temperatureCalculated, "0"])
                        else:
                            print("Boooo0o0")

                    if parsedBeginningLetter == "B":

                        app.updateLightLabel(parsedInDecimal)

                        if lastMovementDirection == "Up":
                            with open("C:/Temp/test_data_Light.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, "0", parsedInDecimal])
                        elif lastMovementDirection == "Down":
                            with open("C:/Temp/test_data_Light.csv", "a") as f:
                                writer = csv.writer(f, delimiter=",")
                                writer.writerow([time.time(), count, parsedBeginningLetter, parsedInDecimal, "0"])

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

#ser.close()


