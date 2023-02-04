import threading
import time
import serial
import inspect
import os
import sys
import stat
import subprocess
import array

# dmesg | grep tty
# sudo chmod 666 /dev/ttyUSB0


class Serial_Receiver(threading.Thread):
    def __init__(self, sercomm):
        threading.Thread.__init__(self)
        self.num = 0
        self.quit = False
        self.sercomm = sercomm

    def run(self):
        while True:
            data = self.sercomm.read_all()
            if data:
                # rec_str=data.decode('utf-8')
                rx_hex = []
                for n in data:
                    rx_hex.append(hex(n))
                print('rx:', rx_hex)
            self.num += 1
            time.sleep(0.3)
            if self.quit:
                break

    def exit(self):
        self.quit = True


class SerialComm():
    def __init__(self):
        super(SerialComm, self).__init__()

    def init_parameter(self, port=None, baudrate=9600):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=0)
        self.serial_rx = Serial_Receiver(self.serial)
        self.serial_rx.start()

    def tx_strmsg(self, msg):
        msg_bytes = bytes(msg, 'ascii')
        tx_log = 'tx[%d]: %s' % (len(msg_bytes), msg_bytes)
        print(tx_log)
        self.serial.write(msg_bytes)

    def tx_hex(self, hex_num):
        self.serial.write(hex_num)

    def tx_hexmsg(self, str_nums):
        status = True
        try:
            _int = []
            for str_num in str_nums:
                _int.append(int(str_num, 16))
            for _i in _int:
                if _i > 255:
                    status = False
                    break
            byte_val = bytes(_int)
            self.tx_hex(byte_val)

        except ValueError as e:
            print(e)

    def exit(self):
        self.serial_rx.exit()
        print('serialcomm exit')
