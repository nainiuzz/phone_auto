#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 各模块链接
import sys
import os

project_folder = os.getcwd()[0:os.getcwd().find("ui_auto_test")]
sys.path.append(project_folder + "ui_auto_test\\src")
sys.path.append(project_folder + "ui_auto_test\\src\\touch")
import oper_action
import more_process
import SoaClient


def test_run():
    devices = []
    pool = SoaClient.get_pool()
    for device_list in pool:
        tup = (int(device_list["port"]), device_list["device"])
        devices.append(tup)
    threads = more_process.create_process(devices, oper_action.test_run)
    more_process.start_process(threads[0], threads[1])


if __name__ == '__main__':
    test_run()
