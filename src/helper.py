#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
from appium import webdriver
import configparser
import json
import time
import datetime
import yaml

# QA, ,根据不同的系统，选择不同的配置文件
configFileName = "QA.yml"
projectName = "ui_auto_test"
# 判断是否需要进行配置加载
load_config = False
cp = configparser.ConfigParser()
file_path = os.path.dirname(os.getcwd()).replace('\\', '/')
index = int(file_path.index(projectName))
srcPath = file_path[0:index] + projectName + "/src"
file_path = file_path[0:index] + projectName + "/src/config/" + configFileName


def initial_appium(iphone=0, desired_caps=None, port=None):
    """
    初始化移动端
    Args:
        iphone: 0代表真机，1代表模拟器
        desired_caps: 传入驱动的数据
        port: 端口号
    Returns:
        driver

    """
    global help_appium
    desired_cap = {}
    # 启动appium之前判断进程是否结束
    if port:
        command_executor = "http://localhost:%s/wd/hub" % str(port)
    else:
        command_executor = "http://localhost:4723/wd/hub"
    if iphone == 0:
        if desired_caps:
            desired_cap = desired_caps
        else:
            desired_cap['platformName'] = 'Android'
            desired_cap['platformVersion'] = '4.3'
            desired_cap['deviceName'] = 'SM-N7508V'
            desired_cap['app'] = srcPath + '/common/app-dev-release_70299.apk'
            desired_cap['noReset'] = True
            desired_cap['automationName'] = 'Uiautomator2'
            # desired_cap['wdaLocalPort'] = '4492'
            # desired_cap['appPackage'] = 'com.xingjiabi.shengsheng'
            # desired_cap['appActivity'] = '.ui.LauncherUI'
            # desired_cap['unicodeKeyboard'] = True
            # desired_cap['resetKeyboard'] = False
            # desired_cap['chromeOptions'] = {'androidProcess': 'com.tencent.mm:tools'}  # 驱动H5自动化关键之一
    else:
        desired_cap['platformName'] = 'Android'
        desired_cap['platformVersion'] = '5.1.1'
        desired_cap['deviceName'] = '127.0.0.1:62025'
        desired_cap['app'] = srcPath + '/common/app-dev-release-20180731.apk'
        desired_cap['appPackage'] = 'com.xingjiabi.shengsheng'
        desired_cap['appActivity'] = "com.xingjiabi.shengsheng.app.SplashActivity"
        desired_cap['noReset'] = True
        # 是使用unicode编码方式发送字符串
        desired_cap['unicodeKeyboard'] = True
        # # 将键盘隐藏起来
        desired_cap['resetKeyboard'] = False
        desired_cap['automationName'] = 'Uiautomator2'
        # 意思就是Appium 自动决定获取安装app需要的权限 默认是false
        desired_cap['autoGrantPermissions'] = True
    help_appium = webdriver.Remote(command_executor, desired_cap)

    return help_appium


# 释放selenium对象，关闭driver和chrome进程
def release_appium():
    help_appium.quit()


# 获取appium对象
def get_appium():
    return help_appium


# 获取当前src文件夹的绝对路径
def get_src_path():
    return srcPath.replace('\\', '/')


def get_pytest_param(file_name, option=None):
    """
    定义pytest调试方法参数
    Args:
        file_name: 文件名
        option: 需要添加的操作
    Returns:
        文件名
    """
    html_file = get_src_path() + "/report.html"
    html_file = html_file.replace("/src", "").replace("\\", "/")
    file_name = file_name + " --html=" + html_file
    if option:
        if 'junitxml' in option:
            file_name = file_name + " " + option + get_src_path().replace("/src", "") + "/report.xml"
        else:
            file_name = file_name + " " + option
    print(file_name)
    return file_name


def read_config_item(section, option=None, f=None):
    """
    获取配置文件中某项配置
    Args:
        section: 配置文件的哪块
        option: 配置文件的key
        f: 文件路径

    Returns:
       读取到的值
    """
    global load_config
    if not f:
        f = file_path
        if 'yml' in f:
            yml_detail = read_yml_file(f)
            if option:
                value = yml_detail.get(section)[option]
            else:
                value = yml_detail.get(section)
        else:
            cp.read(f, encoding="utf-8-sig")
            value = str(cp.get(section, option))
        load_config = True
    else:
        if 'yml' in f:
            yml_detail = read_yml_file(f)
            if option:
                value = yml_detail.get(section)[option]
            else:
                value = yml_detail.get(section)
            # value = yml_detail.get(section)[option]
        else:
            # f = file_path[0:index] + projectName + "/src/config/" + f
            cp.read(f, encoding="utf-8-sig")
            value = str(cp.get(section, option))
    return value


def alter_config_item(section, option, value, f=None):
    """
    修改配置文件中某项配置
    Args:
        section: 配置文件的哪块
        option: 配置文件的key
        value: 要修改的值
        f: 文件路径

    Returns:
        修改后的值
    """
    global load_config
    # read_config_item(section, option, f)
    if not f:
        f = file_path
        if not load_config:
            cp.read(f, encoding="utf-8-sig")
            load_config = True
    else:
        f = file_path[0:index] + projectName + "/src/config/" + f
        cp.read(f, encoding="utf-8-sig")
    cp.set(section, option, value)
    fh = open(f, "w")
    cp.write(fh)
    return value


# 重置flag
def init_flag():
    alter_config_item("flag", "compare_flag", '0')
    return True


def read_log_file(file_name):
    """
    读取日志文件
    Args:
        file_name: log名称

    Returns:
        log内容

    """
    log_path = str(get_src_path()) + "/log/" + file_name
    with open(log_path, encoding='UTF-8') as log_file:
        return log_file


def read_json_file(file_name):
    """
    根据绝对路径读取json文件数据
    Args:
        file_name: json文件名
    Returns:
        json的python可读数据

    """

    json_file_path = str(get_src_path()).replace("src", "resource/" + file_name)
    with open(json_file_path, encoding='UTF-8') as json_file:
        data = json.load(json_file)
        return data


def json_data(file_name, key):
    """
    根据文件名读取json文件数据
    Args:
        file_name: 文件名
        key: json根节点的key
    Returns:
        获取出来的数据

    """
    data = read_json_file(file_name)
    return data[key]


def alter_json_data(file_name, data):
    """
    修改json文件数据
    Args:
        file_name: json文件名
        data: 修改的json数据

    Returns:
        修改后的json文件
    """
    json_file_path = str(get_src_path()).replace("src", "resource/" + file_name)
    with open(json_file_path, 'w') as json_file:
        json_detail = json.dump(data, json_file)
        return json_detail


def read_yml_file(files_path):
    """
    读取yml文件内容
    Args:
        files_path: yml文件路径

    Returns:

    """
    with open(files_path, encoding='UTF-8') as xml_file_path:
        data = yaml.load(xml_file_path)
        return data


def alter_yml_file(data, file_paths=None):
    if not file_paths:
        f = file_path
    else:
        f = file_paths
    values = read_yml_file(f)
    values[data.keys()] = data.values()
    # json_file_path = str(get_src_path()).replace("src", "resource/" + file_name)
    with open(f, 'w') as yml_file:
        yml_detail = yaml.dump(data, yml_file)
        return yml_detail


def get_current_time(date_type='%Y-%m-%d %H:%M:%S'):
    """
    获取当前时间
    Args:
        date_type: 日期格式，默认值为：'%Y-%m-%d %H:%M:%S'
                   格式可选择：%y 两位数的年份表示（00-99）
                             %Y 四位数的年份表示（000-9999）
                             %m 月份（01-12）
                             %d 月内中的一天（0-31）
                             %H 24小时制小时数（0-23）
                             %I 12小时制小时数（01-12）
                             %M 分钟数（00=59）
                             %S 秒（00-59）

    Returns:
        获取的当前时间

    """
    return time.strftime(date_type, time.localtime(time.time()))


def alter_current_time(date_type='%Y-%m-%d %H:%M:%S', days=0, hours=0, minutes=0):
    """
    获取当前时间并修改时间
    Args:
        date_type: 日期格式，默认值为：'%Y-%m-%d %H:%M:%S'
        days: 时间差天，默认值为：0
        hours: 时间差小时， 默认值为：0
        minutes: 时间差分钟， 默认值为：0

    Returns:
        修改后的时间
    """
    now = datetime.datetime.now()
    return (now + datetime.timedelta(days=days, hours=hours, minutes=minutes)).strftime(date_type)


if __name__ == '__main__':
    pool = read_config_item("phone_pool")
    print(pool)
    # alter_current_time()
