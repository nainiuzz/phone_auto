#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import helper
import oper_action
from multiprocessing import Process


def create_process(process_list, method):
    """
    增加进程池
    :param process_list: 要线程列表.appium端口和设备id
    :param method: 需要执行的方法
    :return:
    和driver线程池
    """
    server_process = []
    driver_process = []

    for _process_list in process_list:
        # 填写需要跑的方法
        server_process.append(Process(target=servers, args=_process_list))
        driver_process.append(Process(target=method, args=_process_list))
    return server_process, driver_process


def start_process(server_process, driver_process):
    for t in server_process:
        t.start()
    for i in driver_process:
        i.start()


def servers(port, device_id):
    """
    终端命令开启appium服务
    :param port: appium端口
    :param device_id: 设备id
    """
    log_path = helper.srcPath + "/log/" + str(port) + ".log"
    cmd = "appium --address 127.0.0.1 " + " --port " + str(port) + " --bootstrap-port " + str(
        int(port) - 2000) + " -U " + str(device_id) + " --session-override  --log " + str(log_path)
    os.system(cmd)


if __name__ == "__main__":
    devices = []
    device_list = helper.read_config_item("devices")
    for j in range(len(device_list)):
        tup = (device_list[j]["port"], device_list[j]["device"])
        devices.append(tup)
    threads = create_process(devices, oper_action.test_run)
    start_process(threads[0], threads[1])
