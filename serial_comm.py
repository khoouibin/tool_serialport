import threading
import time
import serial
import inspect
import os, sys,stat
import subprocess
import array

# dmesg | grep tty
# sudo chmod 666 /dev/ttyUSB0
class Serial_Receiver(threading.Thread):
    def __init__(self,sercomm):
        threading.Thread.__init__(self)
        self.num = 0
        self.quit = False
        self.sercomm= sercomm

    def run(self):
        while True:
            # print('thread_num:',self.num)
            data = self.sercomm.read_all()
            if data:
                rec_str=data.decode('utf-8')
                hex_list = []
                for n in data:
                    hex_list.append(hex(n))
 
                rec_log = 'rx[%d]: %s'%(len(rec_str),rec_str)
                print(rec_log,hex_list)

            self.num += 1
            time.sleep(0.3)
            if self.quit:
                break

    def exit(self):
        self.quit = True
        #print(inspect.currentframe().f_lineno)
        #print(inspect.currentframe().f_locals)


class SerialComm():
    def __init__(self):
        super(SerialComm, self).__init__()

    def init_parameter(self, port=None, baudrate=9600):
        self.serial = serial.Serial(port=port, baudrate=baudrate,timeout=0)
        self.serial_rx = Serial_Receiver(self.serial)
        self.serial_rx.start()

    def tx_msg(self,msg):
        msg_bytes = bytes(msg,'ascii')
        tx_log = 'Send[%d]: %s'%(len(msg_bytes),msg_bytes)
        print(tx_log)
        self.serial.write(msg_bytes)
        
    def exit(self):
        self.serial_rx.exit()
        print('serialcomm exit')
