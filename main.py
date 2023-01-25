import sys
import time
import json
import os
from termcolor import colored
from serial_comm import SerialComm

serialcomm = SerialComm()


def cli():
    while True:
        try:
            cli_input = input(">> ")
            cli_input_list = cli_input.split(" ")

            if len(cli_input_list) > 0:
                if cli_input_list[0] == 'q':
                    break
                elif cli_input_list[0] == 'tx':
                    if len(cli_input_list) == 2:
                        serialcomm.tx_msg(cli_input_list[1])
                    else:
                        continue
            else:
                pass
        except KeyboardInterrupt:
            print(colored('key interrupt occur !!!', 'red'))
            break

def main():
    tty_device = '/dev/ttyUSB0'
    i_baudrate = 9600
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
            i += 1

    log = 'tty dev=%s, baudrate=%d' % (tty_device, i_baudrate)
    print(log)
    serialcomm.init_parameter(tty_device,i_baudrate)
    cli()
    serialcomm.exit()
    sys.exit(0)

if __name__ == '__main__':
    main()
