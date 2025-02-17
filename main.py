import sys
import time
import json
import os
from termcolor import colored
from serial_comm import Serial_Transmitter
import serial.tools.list_ports
# serialcomm = Serial_Transmitter()


def cli_help():
    help_doc = ''
    help_doc += 'q : quit program'+os.linesep
    help_doc += 'tx: send data to serial port'+os.linesep
    help_doc += '    (1) tx str xxxxx xxx'+os.linesep
    help_doc += '    (2) tx hex 12 34 56 78'+os.linesep
    help_doc += 'set lc12s -setting parameter for lc12s'
    print(help_doc)


def cli(serialcomm):
    while True:
        try:
            cli_input = input(">> ")
            cli_input_list = cli_input.split(" ")

            if len(cli_input_list) > 0:
                if cli_input_list[0] == 'q':
                    break
                elif cli_input_list[0] == 'help':
                    cli_help()
                elif cli_input_list[0] == 'tx':
                    if len(cli_input_list) < 3:
                        continue
                    else:
                        if cli_input_list[1] == 'str':
                            cli_str_split = cli_input.split("str ")
                            if len(cli_str_split) == 2:
                                serialcomm.tx_str(cli_str_split[1])

                        elif cli_input_list[1] == 'hex':
                            str_hexes = []
                            for n in range(2, len(cli_input_list)):
                                str_hexes.append(cli_input_list[n])

                            serialcomm.tx_hexmsg(str_hexes)

                        elif cli_input_list[1] == 'modbus':
                            str_nums = []
                            for n in range(2, len(cli_input_list)):
                                str_nums.append(cli_input_list[n])

                            serialcomm.tx_hexmsg_crc16(str_nums)

                        else:
                            continue

                elif cli_input_list[0] == 'set':
                    if cli_input_list[1] == 'lc12s':
                        serialcomm.tx_lc12s_settings()

            else:
                pass
        except KeyboardInterrupt:
            print(colored('key interrupt occur !!!', 'red'))
            break


def main():
    serial_ports = []
    for port in serial.tools.list_ports.comports():
        port_info = {'device': port.device, 'name': port.name}
        serial_ports.append(port_info)

    tty_device = '/dev/ttyUSB0'
    i_baudrate = 781250
    b_skip_serial_setting = False

    for port in serial_ports:
        print('device:', port['device'])
        cmd = "chmod 666 %s" % (port['device'])
        p = os.system('echo %s|sudo -S %s' % ('orisol', cmd))

    if len(serial_ports) > 0:
        for i, port in enumerate(serial_ports):
            if i == 0:
                pri_serial = Serial_Transmitter(port['name'])
                pri_serial.init_parameter(
                    port['device'], i_baudrate, b_skip_serial_setting)
            else:
                sec_serial = Serial_Transmitter(port['name'])
                sec_serial.init_parameter(
                    port['device'], i_baudrate, b_skip_serial_setting)
                break

        cli(pri_serial)
        for i, port in enumerate(serial_ports):
            if i == 0:
                pri_serial.exit()
            else:
                sec_serial.exit()
                break

    sys.exit(0)


if __name__ == '__main__':
    main()
