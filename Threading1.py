"""
Threading 1 shows the firing of threads from a GUI, attempting (and failing) to close them.
"""

from tkinter import Tk, Label, Button
import threading
import time
import requests
import queue

testTest = None

class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=self.stopProgram)
        self.close_button.pack()

    def messagePrint(self):
        while True:
            for i in range(10):
                print("Message " + str(i))
                time.sleep(0.5)
            threading.Thread.join(threading.main_thread())

    def greet(self):
        print("Greetings!")



        testTest = threading.Thread(target=self.messagePrint).start()








    def stopProgram(self):
        print("Try to stop")
        #print(threading.Thread(testTest).is_alive())





root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()