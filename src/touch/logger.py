#!/usr/bin/env python
# -*- coding:utf-8 -*-

import logging
import logging.config
from logging.handlers import RotatingFileHandler
import threading
import os
import configparser
import helper

projectName = "ui_auto_test"
cp = configparser.ConfigParser()
file_path = os.path.dirname(os.getcwd())
index = int(file_path.index(projectName))
srcPath = file_path[0:index] + projectName + "\\src"


class LogSignleton(object):
    def __init__(self, log_config):
        pass

    def __new__(cls, log_config):
        mutex = threading.Lock()
        mutex.acquire()  # 上锁，防止多线程下出问题
        if not hasattr(cls, 'instance'):
            cls.instance = super(LogSignleton, cls).__new__(cls)
            helper.read_config_item("LOGGING", "max_bytes_each", log_config)
            # config = configparser.ConfigParser()
            # config.read(log_config, encoding="utf-8-sig")
            cls.log_filename = os.path.join(srcPath, 'log', 'touch.log')
            cls.instance.max_bytes_each = int(helper.read_config_item("LOGGING", "max_bytes_each", log_config))
            cls.instance.backup_count = int(helper.read_config_item("LOGGING", "backup_count", log_config))
            cls.instance.log_level_in_console = int(
                helper.read_config_item("LOGGING", "log_level_in_console", log_config))
            cls.instance.log_level_in_logfile = int(
                helper.read_config_item("LOGGING", "log_level_in_logfile", log_config))
            cls.instance.logger_name = helper.read_config_item("LOGGING", "logger_name", log_config)
            cls.instance.console_log_on = int(helper.read_config_item("LOGGING", "console_log_on", log_config))
            cls.instance.logfile_log_on = int(helper.read_config_item("LOGGING", "logfile_log_on", log_config))
            cls.instance.level_name = helper.read_config_item("LOG_DETAIL", "level_name", log_config)
            cls.instance.asc_time = helper.read_config_item("LOG_DETAIL", "asc_time", log_config)
            cls.instance.project_name = helper.read_config_item("LOG_DETAIL", "project_name", log_config)
            cls.instance.file_name = helper.read_config_item("LOG_DETAIL", "file_name", log_config)
            cls.instance.line_no = helper.read_config_item("LOG_DETAIL", "line_no", log_config)
            cls.instance.message = helper.read_config_item("LOG_DETAIL", "message", log_config)
            cls.instance.logger = logging.getLogger(cls.instance.logger_name)
            cls.instance.__config_logger()
        mutex.release()
        return cls.instance

    def get_logger(self):
        # self.__config_logger()
        return self.logger

    def __config_logger(self):
        # 设置日志格式
        fmt_detail = '%s | %s | %s | %s |%s | %s ' % (
            self.level_name.replace('|', '%'), self.asc_time.replace('|', '%'), self.project_name,
            self.file_name.replace('|', '%'),
            self.line_no.replace('|', '%'), self.message.replace('|', '%'))
        fmt = fmt_detail
        formatter = logging.Formatter(fmt, datefmt='%Y-%m-%d %H:%M:%S')

        if self.console_log_on == 1:  # 如果开启控制台日志
            self.console = logging.StreamHandler()
            self.console.setFormatter(formatter)
            self.logger.addHandler(self.console)
            self.logger.setLevel(self.log_level_in_console)

        if self.logfile_log_on == 1:  # 如果开启文件日志
            self.rt_file_handler = RotatingFileHandler(self.log_filename, maxBytes=self.max_bytes_each,
                                                       backupCount=self.backup_count, encoding="UTF-8")
            self.rt_file_handler.setFormatter(formatter)
            self.logger.addHandler(self.rt_file_handler)
            self.logger.setLevel(self.log_level_in_logfile)


file_name = 'logging.yml'
config_dir = os.path.join(srcPath, 'config', file_name)
logsignleton = LogSignleton(config_dir)
logger = logsignleton.get_logger()
