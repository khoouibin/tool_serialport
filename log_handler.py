import os
import json
import logging
import coloredlogs
from datetime import datetime
from termcolor import colored

currDateTime = datetime.now()
logfile_limit = 3


def change_owner(path, uid=1000):
    os.chown(path, uid, uid)


class log_handler:
    __init_parameter = False

    def __new__(cls, *args, **kw):
        if not hasattr(cls, "_instance"):
            orig = super(log_handler, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance

    def init_parameter(self, app_path):
        if self.__init_parameter == True:
            return
        print('log_handler-init_parameter-app_path:', app_path)
        self.logname = "ser_%s.log" % (currDateTime.strftime("%Y-%m-%d-%H-%M"))
        self.log_dir = os.path.join(app_path, "LOG")
        self.log_dok_dir = os.path.join(app_path, "LOG", "SERIAL")
        if not os.path.isdir(self.log_dir):
            os.mkdir(self.log_dir)
            change_owner(self.log_dir)
        if os.path.isdir(self.log_dir):
            if not os.path.isdir(self.log_dok_dir):
                os.mkdir(self.log_dok_dir)
                change_owner(self.log_dok_dir)
            self.logname_abs = os.path.join(self.log_dok_dir, self.logname)
            logging.basicConfig(
                level=logging.INFO,
                format="%(asctime)s-[%(levelname)s]-%(message)s",
                handlers=[
                    logging.FileHandler(self.logname_abs),
                    logging.StreamHandler()
                ]
            )
            logger = logging.getLogger(__name__)
            coloredlogs.install(level='DEBUG', logger=logger)

            logging.info("log started")
            logging.info("log dok dir:%s" % (self.log_dok_dir))
            logging.info("log file name:%s" % (self.logname_abs))
            self.log_filebounded(file_limit=logfile_limit)
            self.__init_parameter = True

    def get_dok_log_path(self):
        return self.log_dok_dir

    def get_filelist(self, search_path, ext_filter_list=None):
        filelist = []
        for root, dirs, files in os.walk(top=search_path, topdown=False):
            for file in files:
                if root == search_path:
                    if ext_filter_list == None:
                        filelist.append(file)
                    else:
                        filename, dot_ext = os.path.splitext(file)
                        ext = dot_ext[1:]
                        if ext in ext_filter_list:
                            filelist.append(filename)
        filelist.sort(reverse=False)
        return filelist

    def log_filebounded(self, file_limit):
        filelist = self.get_filelist(self.log_dok_dir)
        print(filelist)
        if len(filelist) > file_limit:
            remove_nums = len(filelist) - file_limit
            removed = 0
            for idx, file in enumerate(filelist):
                abs_filepath = os.path.join(self.log_dok_dir, file)
                os.remove(abs_filepath)
                removed += 1
                if removed >= remove_nums:
                    break

    def log_message(self, print_terminal=True, color='green', module=None, message=''):
        if self.__init_parameter != True:
            return

        if module == None:
            module = __name__

        msg = "%s - %s" % (module, message)
        logging.debug(msg)
