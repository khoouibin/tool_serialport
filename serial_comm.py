import threading
import time
import serial
import inspect
import os
import sys
import stat
import subprocess
import array
from log_handler import log_handler

# dmesg | grep tty
# sudo chmod 666 /dev/ttyUSB0

ser_log_handler = log_handler()
ser_log_handler.init_parameter(os.getcwd())


class Serial_Receiver(threading.Thread):
    def __init__(self, sercomm):
        threading.Thread.__init__(self)
        self.num = 0
        self.quit = False
        self.sercomm = sercomm
        self.sertx = Serial_Transmitter()

    def run(self):
        while True:
            rx_bytes = self.sercomm.read_all()
            if rx_bytes:
                # rec_str=data.decode('utf-8')
                rx_hex = []
                for rx_byte in rx_bytes:
                    rx_hex.append("{:02x}".format(rx_byte))
                log = 'rx[%d]:%s' % (len(rx_hex), rx_hex)
                ser_log_handler.log_message(
                    module='rx_log', color='magenta', message='%s' % (log))

            self.num += 1
            time.sleep(0.3)
            if self.quit:
                break

    def exit(self):
        self.quit = True


class Serial_Transmitter():
    def __init__(self):
        super(Serial_Transmitter, self).__init__()

    def init_parameter(self, port=None, baudrate=9600, b_skip_init=False):
        self.skip_init = b_skip_init
        self.log_handler = log_handler()
        self.log_handler.init_parameter(os.getcwd())

        if self.skip_init == False:
            self.serial = serial.Serial(
                port=port, baudrate=baudrate, timeout=0)
            self.serial_rx = Serial_Receiver(self.serial)
            self.serial_rx.start()

    def log_hexmsg(self, hex_bytes, print_log=False):
        hexmsg = hex_bytes.hex()
        hexlist = []
        _str = ''
        for idx, _hex in enumerate(hexmsg):
            _str += _hex
            if idx % 2 != 0:
                hexlist.append(_str)
                _str = ''
        log = 'tx[%d]:%s' % (len(hexlist), hexlist)
        ser_log_handler.log_message(
            module='tx_log', color='cyan', message='%s' % (log))

    def tx_str(self, str_msg):
        msg_bytes = bytes(str_msg, 'ascii')
        self.log_hexmsg(msg_bytes, print_log=True)
        if self.skip_init == False:
            self.serial.write(msg_bytes)

    def tx_hex(self, hex_bytes):
        self.log_hexmsg(hex_bytes, print_log=True)
        if self.skip_init == False:
            self.serial.write(hex_bytes)

    def tx_hexmsg(self, str_hexes):
        try:
            hexlist = []
            for str_hex in str_hexes:
                _int = int(str_hex, 16)
                if _int <= 255:
                    hexlist.append(int(str_hex, 16))
                else:
                    raise ValueError("out of range 0~255:", _int)
            self.tx_hex(bytes(hexlist))

        except ValueError as e:
            ser_log_handler.log_message(
                module='tx_log', color='red', message='%s' % (e))

    def crc16_cal(self, int_nums):
        crc = 0xffff
        high_byte = 0
        low_byte = 0

        for int_num in int_nums:
            crc_byte = int_num & 0x00ff
            crc ^= crc_byte
            for i in range(8):
                if crc & 0x0001 != 0:
                    crc >>= 1
                    crc ^= 0xa001
                else:
                    crc >>= 1
        high_byte = (crc >> 8) & 0x00ff
        low_byte = crc & 0x00ff
        return high_byte, low_byte

    def tx_hexmsg_crc16(self, str_nums):
        status = True
        try:
            _int = []
            for str_num in str_nums:
                #print('str_num:', str_num)
                _int.append(int(str_num, 16))

            high_byte, low_byte = self.crc16_cal(_int)
            _int.append(low_byte)
            _int.append(high_byte)
            for _i in _int:
                if _i > 255:
                    status = False
                    break
            byte_val = bytes(_int)
            self.tx_hex(byte_val)
        except ValueError as e:
            print(e)

    def tx_lc12s_settings(self):
        settings = {
            'setting_1': 'aa',
            'setting_2': '5a',
            'setting_3': '22',  # self id-1
            'setting_4': '33',  # self id-0
            'setting_5': '11',  # net  id-1
            'setting_6': '22',  # net  id-0
            'setting_7': '00',  # nc
            'setting_8': '00',  # rf power
            'setting_9': '00',  # nc
            'setting_10': '04',  # baud 9600bps
            'setting_11': '00',
            'setting_12': '64',  # rf channel
            'setting_13': '00',  # nc
            'setting_14': '00',  # nc
            'setting_15': '00',  # nc
            'setting_16': '12',  # lenght
            'setting_17': '00',
        }

        setting_list = []
        for i in range(1, 18):
            setting_list.append(int(settings['setting_'+str(i)], 16))
        chksum = 0
        for i in range(len(setting_list)):
            chksum += setting_list[i]
        chksum &= 0x00ff
        setting_list.append(chksum)

        setting_hex = []
        for i in setting_list:
            setting_hex.append("{:02x}".format(i))
        byte_setting_list = bytes(setting_list)
        print('tx[{}]:{}'.format(len(setting_hex), setting_hex))
        self.tx_hex(byte_setting_list)

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
        if self.skip_init == False:
            self.serial_rx.exit()
        print('serialcomm exit')
