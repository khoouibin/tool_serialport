import sys
import time
import json
import os
from termcolor import colored
from serial_comm import Serial_Transmitter

serialcomm = Serial_Transmitter()


def cli_help():
    help_doc = ''
    help_doc += 'q : quit program'+os.linesep
    help_doc += 'tx: send data to serial port'+os.linesep
    help_doc += '    (1) tx str xxxxx xxx'+os.linesep
    help_doc += '    (2) tx hex 12 34 56 78'+os.linesep
    help_doc += 'set lc12s -setting parameter for lc12s'
    print(help_doc)


def cli():
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
    tty_device = '/dev/ttyUSB0'
    i_baudrate = 9600
    b_skip_serial_setting = False
    if len(sys.argv) > 1:
        argc = len(sys.argv)
        i = 0
        enum_argv = enumerate(iter(sys.argv))
        while i < argc:
            index, argv = next(enum_argv)
            if argv == '-tty':
                if index+1 == argc:
                    break
                else:
                    tty_device = next(enum_argv)[1]
                    i += 1
            elif argv == '-baud':
                if index+1 == argc:
                    break
                else:
                    i_baudrate = int(next(enum_argv)[1])
                    i += 1
            elif argv == '-sim':
                b_skip_serial_setting = True
                if index+1 == argc:
                    break
                else:
                    i += 1

            i += 1

    log = 'tty dev=%s, baudrate=%d, sim=%d' % (
        tty_device, i_baudrate, b_skip_serial_setting)
    print(log)
    serialcomm.init_parameter(tty_device, i_baudrate, b_skip_serial_setting)
    cli()
    serialcomm.exit()
    sys.exit(0)


if __name__ == '__main__':
    main()
