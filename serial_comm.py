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
                print('rx[{}]:{}'.format(len(rx_hex),rx_hex))
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
            print(byte_val)
            self.tx_hex(byte_val)

        except ValueError as e:
            print(e)

    def tx_lc12s_settings(self):
        settings = {
            'setting_1': 'aa',
            'setting_2': '5a',
            'setting_3': '00',
            'setting_4': '00',
            'setting_5': '00',
            'setting_6': '00',
            'setting_7': '00',
            'setting_8': '00',
            'setting_9': '00',
            'setting_10': '04',
            'setting_11': '00',
            'setting_12': '0a',
            'setting_13': '00',
            'setting_14': '00',
            'setting_15': '00',
            'setting_16': '12',
            'setting_17': '00',
        }

        int_list = []
        for i in range(1, 18):
            int_list.append(int(settings['setting_'+str(i)], 16))
        chksum = 0
        for i in range(len(int_list)):
            chksum += int_list[i]
        chksum &= 0x00ff
        int_list.append(chksum)
        byte_int_list = bytes(int_list)
        print('tx[{}]:{}'.format(len(byte_int_list),byte_int_list))
        self.tx_hex(byte_int_list)
        # str_01='aa'
        # str_02='5a'

        # str_03='01'
        # str_04='01'
        # str_05='01'
        # str_06='01'

        # str_07='00'
        # str_08='01'
        # str_09='00'
        # str_10='04'

        # str_11='00'
        # str_12='12'

        # str_13='00'

        # str_14='14'
        # str_15='15'

        # str_16='12'
        # str_17='00'

    def exit(self):
        self.serial_rx.exit()
        print('serialcomm exit')
