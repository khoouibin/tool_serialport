import threading
import time
import serial
import inspect
import os, sys,stat
import subprocess

# dmesg | grep tty


class Serial_Receiver(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.num = 0
        self.quit = False

    def run(self):
        while True:
            # print('thread_num:',self.num)
            self.num += 1
            time.sleep(1)
            if self.quit:
                break

    def exit(self):
        self.quit = True
        print(inspect.currentframe().f_lineno)
        print(inspect.currentframe().f_locals)


class SerialComm():
    def __init__(self):
        super(SerialComm, self).__init__()

    def init_parameter(self, port=None, baudrate=9600):
        _command = "sudo chmod 666 " + port
        subprocess.Popen(_command, shell=True, stderr=subprocess.STDOUT)
        self.serial = serial.Serial(port=port, baudrate=baudrate)
        print(self.serial.name)
        self.serial_rx = Serial_Receiver()
        self.serial_rx.start()

    def exit(self):
        self.serial_rx.exit()
        print('serialcomm exit')
