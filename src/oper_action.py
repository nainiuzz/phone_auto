#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import helper
import oper
import check
import time
import json
import paramiko
import xml.etree.ElementTree as ET
import requests
import read_files
import send_msg
import SoaClient
import clean
from multiprocessing import Lock
import login


class SaveResult(object):
    def __init__(self):
        self.result_info = []
        self.result_status = []

    def write_result(self, message):
        self.result_info.append(str(message))

    def write_status(self, status):
        self.result_status.append(str(status))

    def get_result(self):
        result_detail = ";".join(self.result_info)
        return result_detail

    def get_status(self):
        status_detail = ";".join(self.result_status)
        if "0" in status_detail:
            status = "0"
        else:
            status = "1"
        return status


class RunXml(object):
    def __init__(self, xml_file_path, write_result, write_status, save_param, log_message=None, flag=None, port=None):
        """
         解析xml文件动作,触发对应操作
        Args:
            xml_file_path: xml文件名
            write_result: SaveResult.write_result，存储结果信息
            write_status: SaveResult.write_status，存储结果状态
            log_message: 规定日志格式
            flag: 当前置用例被调用执行时判定必须执行
        """
        self.xml_file_path = xml_file_path
        self.log_message = log_message
        self.flag = flag
        self.xml_detail = read_xml(self.xml_file_path)
        self.save_param = save_param
        self.get_dict_data = save_param.get_dict_data()
        self.save_value = save_param.save_value
        self.write_result = write_result
        self.write_status = write_status
        self.port = port

    def run(self, result_message=None):
        """
        判断xml脚本的属性，属于前置后置或者普通用例
        """
        for key, value in self.xml_detail.items():
            if "case-type" == key:
                if self.flag:
                    types = "1"
                else:
                    types = value
                if types == "1":
                    # 加入判定登录时选择对应账号登录
                    if "Login/Login" in self.xml_file_path:
                        try:
                            login.login_read_xml(self.xml_file_path, self.port)
                            self.write_result("端口：%s 登录成功！" % self.port)
                            self.write_status("1")
                            oper.log("端口：%s 登录成功！" % self.port)
                        except Exception as e:
                            self.write_result("端口：%s 登录失败！原因为：%s" % (self.port, str(e)))
                            self.write_status("1")
                            oper.log("端口：%s 登录失败！原因为：%s" % (self.port, str(e)), 2)
                    else:
                        self.run_case(result_message)
                elif types == "3":
                    self.write_result("测试用例为后置用例无需执行")
                    self.write_status("1")
                    oper.log("测试用例为后置用例无需执行")
                else:
                    self.write_result("测试用例为前置用例无需执行")
                    self.write_status("1")
                    oper.log("测试用例为前置用例无需执行")

    def run_case(self, result_message=None):
        """
        执行用例步骤

        """
        i = 1
        for xml_key, xml_value in self.xml_detail["cases"].items():
            oper.log("执行测试用例【" + str(xml_key) + "】第" + str(i) + "个测试用例", formats=self.log_message)
            self.run_before_case(xml_value)
            self.run_step(xml_key, xml_value, result_message)
            self.run_after_case(xml_value)

    def run_before_case(self, xml_value):
        """
        运行前置用例
        Args:
            xml_value: 解析xml cases级别的value值

        """
        if "case-beforecases" in xml_value.keys():
            j = 1
            for before_key, before_value in xml_value["case-beforecases"].items():
                if "beforecase-path" in before_value.keys():
                    oper.log("执行测试前置用例【" + str(before_value["beforecase-path"]) + "】",
                             formats=self.log_message)
                    try:
                        run_init = RunXml(before_value["beforecase-path"], self.write_result, self.write_status,
                                          self.save_param, log_message=self.log_message, flag=1, port=self.port)
                        run_init.run("执行测试前置用例【" + str(before_value["beforecase-path"]) + "】")
                    except Exception as e:
                        oper.log("执行测试前置用例【" + str(before_value["beforecase-path"]) + "】失败，原因是：" + str(
                            e), 2, formats=self.log_message)
                        self.write_result("执行测试前置用例【" + str(before_value["beforecase-path"]) + "】失败，原因是：" + str(
                            e))
                        self.write_status("0")
                        pass
                j += 1
                oper.log("执行前置用例【" + str(before_value["beforecase-path"]) + "】完成！", formats=self.log_message)
            del xml_value["case-beforecases"]

    def run_step(self, xml_key, xml_value, result_message=None):
        """
        运行脚本步骤
        Args:
            xml_key: 解析xml cases级别的key值
            xml_value: 解析xml cases级别的value值
            result_message: 执行结果的前缀信息

        """
        case_key = ""
        if result_message:
            case_id = str(result_message)
        else:
            case_id = "执行测试用例【" + str(xml_key) + "】"
        try:
            for case_key, case_value in list(xml_value.items()):
                if "step" in case_key:
                    oper.log(case_id + "的第" + str(case_key) + "个用例步骤", formats=self.log_message)
                    action = XmlAction(case_value, self.write_result)
                    action.xml_action(self.get_dict_data, self.save_value)
            oper.log('运行成功', formats=self.log_message)
            self.write_result("成功")
            self.write_status("1")
        except Exception as e:
            oper.log(case_id + "的第" + str(case_key) + "个用例步骤失败，原因是：" + str(
                e), 2, formats=self.log_message)
            if str(e):
                detail = str(e)
            else:
                detail = ""
            self.write_result(
                str(case_id + "的第" + str(case_key) + "个用例步骤失败，原因是：" + detail))
            if result_message:
                self.write_status("1")
            else:
                self.write_status("0")

    def run_after_case(self, xml_value):
        """
        运行后置用例
        Args:
            xml_value: 解析xml cases级别的value值

        """
        if "case-aftercases" in xml_value.keys():
            for after_key, after_value in xml_value["case-aftercases"].items():
                if "aftercase-path" in after_value.keys():
                    oper.log("执行后置用例【" + str(after_value["aftercase-path"]) + "】", formats=self.log_message)
                    try:
                        run_init = RunXml(after_value["aftercase-path"], self.write_result, self.write_status,
                                          self.save_param, log_message=self.log_message, flag=1, port=self.port)
                        run_init.run("执行后置用例【" + str(after_value["aftercase-path"]) + "】")
                    except Exception as e:
                        oper.log("执行后置用例【" + str(after_value["aftercase-path"]) + "】失败，原因是：" + str(
                            e), 2, formats=self.log_message)
                        self.write_result("执行后置用例【" + str(after_value["aftercase-path"]) + "】失败，原因是：" + str(
                            e))
                        self.write_status("0")
                        pass
                oper.log("执行测试用例【" + str(after_value["aftercase-path"]) + "】的后置用例执行完成！", formats=self.log_message)
            del xml_value["case-aftercases"]


class XmlAction(object):
    def __init__(self, oper_detail, write_result):
        """
        # xml文件动作分析
        Args:
            oper_detail: xml的操作信息，如{'oper': 'oper', 'oper_action'}
            write_result: 操作动作需要传给结果的数据
        """
        self.operate = {
            'oper': self.oper_select,
            'action': self.action_select,
            'keyboard': self.keyboard_select,
            'assert': self.assert_select,
            'cal': self.cal_select
        }
        self.oper = {
            'clear': oper.clear,
            'send_keys': oper.send_keys,
            'click': oper.click,
            'driver_click': oper.driver_wait_click,
            'continuous_click': oper.continuous_click,
            'get_text': oper.get_text,
            'get_attr': oper.get_attr,
            'driver_get_text': oper.driver_wait_get_text,
            'driver_get_attr': oper.driver_wait_get_attr,
            'wait_element': check.wait_element,
            'wait_element_disappear': check.wait_element_disappear,
            'wait_text': check.wait_text,
            'wait_text_disappear': check.wait_text_disappear,
            'wait': time.sleep,
            'log': oper.log,
            'switch_to_webview': oper.switch_to_webview,
            'switch_to_native': oper.switch_to_native,
            'get_page_resource': oper.get_page_resource
        }
        self.action = {
            'action_tap': oper.action_tap,
            'action_tap_xy': oper.action_tap,
            'action_press': oper.action_press,
            'action_press_xy': oper.action_press,
            'action_long_press': oper.action_long_press,
            'action_long_press_xy': oper.action_long_press,
            'action_slither': oper.action_slither,
            'action_slither_xy': oper.action_slither,
            'action_multi': oper.action_multi,
            'action_multi_xy': oper.action_multi,
            'action_wait': oper.action_wait,
            'swipe_up': oper.swipe_up,
            'swipe_down': oper.swipe_down,
            'swipe_left': oper.swipe_left,
            'swipe_right': oper.swipe_right
        }
        self.keyboard = {
            'hide_keyboard': oper.hide_keyboard,
            'key_event': self.key_event,
            'input_key_event': self.input_key_event
        }
        self.asserts = {
            'exist_element': check.assert_exist_element,
            'exist_text': check.assert_exist_text,
            'exist_toast': check.assert_exist_toast,
            'element_disappear': check.assert_not_exist_element,
            'text_disappear': check.assert_not_exist_text,
            'toast_disappear': check.assert_not_exist_toast,
            'equal': self.equal,
            "notequal": self.notequal
        }
        self.cal = {
            'add': oper.CalStyle().add,
            'sub': oper.CalStyle().sub,
            'mul': oper.CalStyle().mul,
            'div': oper.CalStyle().div,
            'cal_equal': oper.CalStyle().equal,
            "cal_notequal": oper.CalStyle().notequal,
            'cal_greater_than': oper.CalStyle().greater_than,
            "cal_greater_than_equal": oper.CalStyle().greater_than_equal,
            'cal_less_than': oper.CalStyle().less_than,
            "cal_less_than_equal": oper.CalStyle().less_than_equal
        }
        self.oper_detail = oper_detail
        self.save_param = {}
        self.write_result = write_result

    def xml_action(self, get_dict_data, save_value):
        """
        判断第一层操作
        """
        if self.oper_detail['oper'] in self.operate.keys():
            self.save_param = get_dict_data
            key = self.oper_detail["oper"]
            value = self.operate.get(key)
            response = value()
            # 存储变量
            if response:
                for key, value in response.items():
                    save_value(key, value)
        else:
            oper.log("传入操作oper的值错误无法匹配，错误值为【" + str(self.oper_detail['oper']) + "】", 2)

    def oper_select(self):
        """
        判断第二层操作动作，点击 输入之类
        """
        if self.oper_detail['oper_action'] in self.oper.keys():
            key = self.oper_detail["oper_action"]
            value = self.oper.get(key)
            index = self.oper_select_detail(key, value)
            if 'get' in key:
                return index
        else:
            oper.log("传入操作oper_action的值错误无法匹配，错误值为【" + str(self.oper_detail['oper_action']) + "】", 2)

    def action_select(self):
        """
        判断第二层操作动作，模拟手指动作
        """
        if self.oper_detail['oper_action'] in self.action.keys():
            key = self.oper_detail["oper_action"]
            value = self.action.get(key)
            self.action_select_detail(key, value)
        else:
            oper.log("传入操作oper_action的值错误无法匹配，错误值为【" + str(self.oper_detail['oper_action']) + "】", 2)

    def keyboard_select(self):
        """
        判断第二层操作动作，物理键盘的操作
        """
        if self.oper_detail['oper_action'] in self.keyboard.keys():
            key = self.oper_detail["oper_action"]
            value = self.keyboard.get(key)
            value()
        else:
            oper.log("传入操作oper_action的值错误无法匹配，错误值为【" + str(self.oper_detail['oper_action']) + "】", 2)

    def assert_select(self):
        """
        判断第二层操作动作，断言
        """
        if self.oper_detail['oper_action'] in self.asserts.keys():
            key = self.oper_detail["oper_action"]
            value = self.asserts.get(key)
            self.assert_select_detail(key, value)
        else:
            oper.log("传入操作oper_action的值错误无法匹配，错误值为【" + str(self.oper_detail['oper_action']) + "】", 2)

    def cal_select(self):
        """
        判断第二层操作动作，计算
        """
        if self.oper_detail['oper_action'] in self.cal.keys():
            index = {}
            key = self.oper_detail["oper_action"]
            value = self.cal.get(key)
            value_1 = self.dispose_cal(self.for_param()['value_1'])
            value_2 = self.dispose_cal(self.for_param()['value_2'])
            if 'cal' not in key:
                sign = self.for_param()['cal_sign'].replace("{", "").replace("}", "")
                index[sign] = value(value_1, value_2)
                return index
            else:
                value(value_1, value_2)
        else:
            oper.log("传入操作oper_action的值错误无法匹配，错误值为【" + str(self.oper_detail['oper_action']) + "】", 2)

    # 处理值是否为变量，若为变量把存储在变量map中的数据赋值。
    def dispose_cal(self, values):
        expect_value = ""
        if ("{{" and "}}") in values:
            expect_sign = values.split("{{")[1].split("}}")[0]
            flag = 0
            for key, value in self.save_param.items():
                if expect_sign in key:
                    flag = 1
                    # 获取到变量值
                    sign_value = self.save_param.get(expect_sign)
                    expect_value = str(values).replace(expect_sign, sign_value).replace("{", "").replace("}", "")
                    break
            if flag == 0:
                oper.log("找不到变量%s的值" % expect_sign, 2)
                raise check.TouchException("找不到变量%s的值" % expect_sign)
        else:
            expect_value = values
        return expect_value

    def assert_select_detail(self, key, value):
        if 'equal' in key:
            value()
        elif 'text' in key or 'toast' in key:
            value(self.dispose_cal(self.for_param()['text']))
        else:
            location = self.dispose_location()
            value(location)

    def equal(self):
        expect_value, actual_value = self.dispose_equal()
        check.compare(expect_value, actual_value)

    def notequal(self):
        expect_value, actual_value = self.dispose_equal()
        check.compare_not(expect_value, actual_value)

    # 处理预期值和实际值是否为变量，若为变量把存储在变量map中的数据赋值。
    def dispose_equal(self):
        expect_value = ""
        actual_value = ""
        if ("{{" and "}}") in self.for_param()['expect_value']:
            expect_sign = str(self.for_param()['expect_value']).split("{{")[1].split("}}")[0]
            flag = 0
            for key, value in self.save_param.items():
                if expect_sign in key:
                    flag = 1
                    # 获取到变量值
                    sign_value = self.save_param.get(expect_sign)
                    expect_value = str(self.for_param()['expect_value']) \
                        .replace(expect_sign, sign_value) \
                        .replace("{", "").replace("}", "")
                    break
            if flag == 0:
                oper.log("找不到预期变量%s的值" % expect_sign, 2)
                raise check.TouchException("找不到预期变量%s的值" % expect_sign)
        else:
            expect_value = self.for_param()['expect_value']
        if ("{{" and "}}") in self.for_param()['actual_value']:
            actual_sign = self.for_param()['actual_value'].split("{{")[1].split("}}")[0]
            flag = 0
            for key, value in self.save_param.items():
                if actual_sign in key:
                    flag = 1
                    # 获取到变量值
                    sign_value = self.save_param.get(actual_sign)
                    actual_value = str(self.for_param()['actual_value']) \
                        .replace(actual_sign, sign_value) \
                        .replace("{", "").replace("}", "")
                    break
            if flag == 0:
                oper.log("找不到实际变量%s的值" % actual_sign, 2)
                raise check.TouchException("找不到实际变量%s的值" % actual_sign)
        else:
            actual_value = self.for_param()['actual_value']
        return expect_value, actual_value

    def oper_select_detail(self, key, value):
        index = {}
        if 'send_keys' in key:
            location = self.dispose_location()
            value(location, self.dispose_cal(self.for_param()['text']))
        elif 'wait_' in key:
            if 'text' in key:
                param = self.dispose_cal(self.for_param()['text'])
            else:
                param = self.dispose_location()
            self.wait_method(self.for_param(), value(param))
        elif 'wait' == key:
            param = int(self.for_param()['time'])
            value(param)
        elif 'log' in key:
            param = self.dispose_cal(self.for_param()['text'])
            oper.log(param)
        elif 'get' in key:
            if 'text' in key:
                location = self.dispose_location()
                param = location
                sign = self.for_param()['sign'].replace("{", "").replace("}", "")
                index[sign] = value(param)
            elif 'page_resource' in key:
                index['page_resource'] = value()
                if index['page_resource']:
                    self.write_result(index['page_resource'])
                else:
                    self.write_result("获取页面资源失败！请排查")
            else:
                sign = self.for_param()['sign'].replace("{", "").replace("}", "")
                param = self.for_param()['values']
                location = self.dispose_location()
                index[sign] = value(location, param)
        elif 'continuous' in key:
            location = self.dispose_location()
            param_number = int(self.for_param()['number'])
            param_time = int(self.for_param()['time'])
            value(location, param_number, param_time)
        elif 'switch_to' in key:
            value()
        else:
            location = self.dispose_location()
            value(location)
        return index

    def action_select_detail(self, key, value):
        if '_xy' in key:
            if ('_slither' or '_multi') in key:
                value(x1=self.for_param()['x_A'], y1=self.for_param()['y_A'], x2=self.for_param()['x_B'],
                      y2=self.for_param()['y_B'])
            elif '_long' in key:
                self.wait_action(self.for_param(),
                                 value(x=self.for_param()['x'], y=self.for_param()['y']))
            else:
                value(x=self.for_param()['x'], y=self.for_param()['y'])
        elif ('_slither' or '_multi') in key:
            if 's' in self.for_param()['styleA']:
                location_a = self.for_param()['styleA'] + ',' + self.for_param()['locationA'] + '[' + self.for_param()[
                    'indexA'] + ']'
            else:
                location_a = self.for_param()['styleA'] + ',' + self.for_param()['locationA']
            if 's' in self.for_param()['styleB']:
                location_b = self.for_param()['styleB'] + ',' + self.for_param()['locationB'] + '[' + self.for_param()[
                    'indexB'] + ']'
            else:
                location_b = self.for_param()['styleB'] + ',' + self.for_param()['locationB']
            value(el1=location_a, el2=location_b)
        elif '_long' in key:
            location = self.dispose_location()
            self.wait_action(self.for_param(),
                             value(location))
        elif '_wait' in key:
            value(int(self.for_param()['time']) * 1000)
        elif 'swipe_' in key:
            value(float(self.for_param()['loc']), int(self.for_param()['time']))
        else:
            location = self.dispose_location()
            value(location)

    def input_key_event(self):
        location = self.dispose_location()
        oper.click(location)
        event_str = oper.KeyEvent(self.for_param()['key_code'])
        event_str.event()

    def key_event(self):
        event_str = oper.KeyEvent(self.for_param()['key_code'])
        event_str.event()

    # 封装方法参数判断方式
    @staticmethod
    def wait_method(oper_detail, func):
        if oper_detail['time']:
            if oper_detail['time'] == 'None':
                times = None
            elif oper_detail['time'] != 'default':
                times = int(oper_detail['time'])
            else:
                times = None
        else:
            times = None

        def inner(*args):
            return func(*args, timeout=times)

        return inner

    # 封装方法参数判断方式
    @staticmethod
    def wait_action(oper_detail, func):
        if oper_detail['time']:
            if oper_detail['time'] == 'None':
                times = None
            elif oper_detail['time'] != 'default':
                times = int(oper_detail['time']) * 1000
            else:
                times = None
        else:
            times = None

        def inner(*args, **kwargs):
            return func(*args, kwargs, duration=times)

        return inner

    def for_param(self):
        param = {}
        if self.oper_detail["param"]:
            for param_key, param_value in self.oper_detail["param"].items():
                for key, value in param_value.items():
                    param[key] = param_value.get(key)
        return param

    def dispose_location(self):
        """
        处理元素定位，看是单一元素 还是多元素
        :return:
        """
        if 's' in self.for_param()['style']:
            location = self.for_param()['style'] + ',' + self.for_param()['location'] + '[' + self.for_param()[
                'index'] + ']'
        else:
            location = self.for_param()['style'] + ',' + self.for_param()['location']
        return location


# 任务内容解析
class TaskAction(object):
    desired_caps = {}

    def __init__(self, res):
        self.desired_caps['platformName'] = helper.read_config_item("desired_caps", "platform_name")
        self.desired_caps['appPackage'] = helper.read_config_item("desired_caps", "app_package")
        self.desired_caps['appActivity'] = helper.read_config_item("desired_caps", "app_activity")
        self.desired_caps['noReset'] = helper.read_config_item("desired_caps", "noreset")
        self.desired_caps['automationName'] = helper.read_config_item("desired_caps", "automationName")
        self.res_body = json.loads(res['msg_body'])
        self.base_info = self.res_body['base_info']
        self.case_info = self.res_body['case_info']
        # self.base_info = helper.read_json_file('task_1.json')['base_info']
        # self.case_info = helper.read_json_file('task_1.json')['case_info']
        self.command = {"command0": 'adb shell ime list -s',  # 列出手机所有的输入法
                        "command1": 'adb shell ime set io.appium.android.ime/.UnicodeIME',  # appium输入法
                        "command2": 'adb shell ime set com.sohu.inputmethod.sogou/.SogouIME',  # 搜狗输入法
                        "command3": 'adb shell ime set com.example.android.softkeyboard/.SoftKeyboard'}  # 模拟器自带英文输入

    def initial_appium(self, port=None, device_name=None):
        if self.base_info['device_type'] == "1":
            self.desired_caps['platformVersion'] = helper.read_config_item("emulator", "device_version")
            if device_name:
                self.desired_caps['deviceName'] = device_name
            else:
                self.desired_caps['deviceName'] = helper.read_config_item("emulator", "device_name")
            if port:
                # 设定并发多进程的时候端口
                self.desired_caps['systemPort'] = 5287 + int(port)
            # 是使用unicode编码方式发送字符串
            self.desired_caps['unicodeKeyboard'] = True
            # 将键盘隐藏起来
            self.desired_caps['resetKeyboard'] = False
            # 设备为模拟器时可以这么用
            dirs = device_name.split(":")[1]
        else:
            self.desired_caps['platformVersion'] = self.base_info['device_version']
            self.desired_caps['deviceName'] = self.base_info['device_name']
            # 是使用unicode编码方式发送字符串
            self.desired_caps['unicodeKeyboard'] = True
            # 将键盘隐藏起来
            self.desired_caps['resetKeyboard'] = False
            if port:
                # 设定并发多进程的时候端口
                self.desired_caps['systemPort'] = 5287 + int(port)
            # 设备为真机时可以这么用
            dirs = device_name
        # 更新共享apk与本地一致
        read_files.exist_apk(str(device_name) + '/' + self.base_info['app'])
        self.desired_caps['app'] = helper.srcPath + '/common/' + str(dirs) + '/' + self.base_info['app']
        helper.initial_appium(desired_caps=self.desired_caps, port=port)
        # 设置输入搜狗输入法
        command = "adb -s %s shell ime set com.sohu.inputmethod.sogou/.SogouIME" % device_name
        os.system(command)

    def read_case_info(self):
        return self.case_info

    def read_base_info(self):
        return self.base_info


def read_linux(file_path, host_name=helper.read_config_item("linux", "host_name"),
               username=helper.read_config_item("linux", "username"),
               password=helper.read_config_item("linux", "password"),
               port=helper.read_config_item("linux", "port")):
    """
    # 读取Linux服务器上文件
    Args:
        file_path: 读取的文件路径，必填项
        host_name: 读取的文件路径，默认值，配置文件helper.read_config_item("linux", "host_name")
        username: 读取的文件路径，默认值，配置文件helper.read_config_item("linux", "username")
        password: 读取的文件路径，默认值，配置文件helper.read_config_item("linux", "password")
        port: 读取的文件路径，默认值，配置文件int(helper.read_config_item("linux", "port")

    Returns:
        读取后的xml文件
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    port = int(port)
    client.connect(host_name, port, username, password, compress=True)
    sftp_client = client.open_sftp()
    path = helper.read_config_item("linux", "file_path") + str(file_path).replace("\\", "")
    remote_file = sftp_client.open(path)
    return remote_file  # 文件路径


def read_http(file_path):
    """
    通过http读取xml文件
    :param file_path: 读取的文件路径，必填项
    :return: 读取后的xml文件
    """
    url = helper.read_config_item("http", "url")
    path = url + str(file_path).replace("\\", "")
    res = requests.get(path, stream=True)
    if res.status_code == 200:
        return res.raw
    else:
        oper.log("【%s】读取xml失败,失败原因：%s" % (file_path, res.text), 2)
        raise check.TouchException("【%s】读取xml失败" % file_path)


def read_xml(xml_file_path):
    """
    读取xml文件
    Args:
        xml_file_path: xml文件名

    Returns:
        字典格式xml的内容
    """
    step_detail = {}
    before_case_detail = {}
    before_cases_detail = {}
    after_case_detail = {}
    after_cases_detail = {}
    param_detail = {}
    params_detail = {}
    xml = {}
    case_detail = {}
    cases_detail = {}
    i, j, k, x, y = 1, 1, 1, 1, 1
    # linux_xml = read_linux(file_path=xml_file_path)
    http_xml = read_http(xml_file_path)
    tree = ET.parse(http_xml)
    root = tree.getroot()  # 打印根元素的tag和属性
    # 遍历xml文档的第二层
    for child in root:
        if "cases" in child.tag:
            for children in child:
                if "case" in children.tag:
                    for case in children:
                        if "case-beforecases" in case.tag:
                            for before_case in case:
                                for _before_case in before_case:
                                    before_case_detail[_before_case.tag] = _before_case.text
                                before_case_step = str(before_case.tag) + str(i)
                                before_cases_detail[before_case_step] = before_case_detail
                                before_case_detail = {}
                                i += 1
                        if "case-aftercases" in case.tag:
                            for after_case in case:
                                for _after_case in after_case:
                                    after_case_detail[_after_case.tag] = _after_case.text
                                after_case_step = str(after_case.tag) + str(j)
                                after_cases_detail[after_case_step] = after_case_detail
                                after_case_detail = {}
                                j += 1
                        if "step" in case.tag:
                            for step in case:
                                if "param" in step.tag:
                                    k = 1
                                    for param in step:
                                        param_detail[param.tag] = str(param.text).replace("\n", "")
                                        k += 1
                                    action = str(step.tag) + str(k)
                                    params_detail[action] = param_detail
                                    step_detail["param"] = params_detail
                                    param_detail = {}
                                    params_detail = {}
                                else:
                                    step_detail[step.tag] = step.text
                            step_step = str(case.tag) + str(x)
                            case_detail[step_step] = step_detail
                            step_detail = {}
                            x += 1
                    case_detail["case-beforecases"] = before_cases_detail
                    case_detail["case-aftercases"] = after_cases_detail
                    # case_detail["step"] = steps_detail
                cases_step = str(children.tag) + str(y)
                cases_detail[cases_step] = case_detail
                y += 1
            xml["cases"] = cases_detail
        else:
            xml[child.tag] = child.text
    oper.log(xml)
    return xml


# 存储变量值
class SaveValue(object):
    def __init__(self):
        self.value_dict = {}

    def save_value(self, key, value):
        self.value_dict[key] = value

    def get_value(self, key):
        value = self.value_dict.get(key)
        return value

    def get_dict_data(self):
        dict_data = self.value_dict
        return dict_data


def run_mq(res, port, device_name):
    result_detail = {"id": "", "case_info": []}
    result_detail = json.dumps(result_detail, ensure_ascii=False)
    result_json = json.loads(result_detail, encoding="utf-8")
    case_info = TaskAction(res).read_case_info()
    task_info = TaskAction(res).read_base_info()
    task_id = task_info["id"]
    result_json["id"] = task_id
    result_case = []
    flag = 0
    init_detail = ""
    lock = Lock()
    try:
        lock.acquire()
        TaskAction(res).initial_appium(port, device_name)
        lock.release()
        # 环境清理
        clean.clean()
    except Exception as e:
        oper.log("appium启动app失败：" + str(e), 2)
        init_detail = "appium启动app失败：" + str(e)
        flag = 1
    for case_id in case_info:
        result_info = SaveResult()
        save_param = SaveValue()
        case_message = {}
        case_message["file_path"] = case_id
        if flag == 1:
            case_message["test_result_info"] = init_detail
            case_message["status"] = "0"
        else:
            try:
                message = "%s | %s | %s | %s | " % (
                    task_info["app"], task_info["id"], task_info["current_version"],
                    case_id)
                oper.log('执行测试用例【' + str(case_id) + '】', formats=message)
                run = RunXml(case_id, result_info.write_result, result_info.write_status,
                             save_param, message, port=port)
                run.run()
            except Exception as e:
                oper.log(e, 2)
                result_info.write_result(str(e))
            case_message["test_result_info"] = result_info.get_result()
            case_message["status"] = result_info.get_status()
        case_message = json.dumps(case_message, ensure_ascii=False)
        result_case.append(case_message)
    try:
        oper.remove_app()
        helper.release_appium()
    except Exception as e:
        oper.log("appium关闭app失败：" + str(e), 2)
    result_json["case_info"] = result_case
    result_json = json.dumps(result_json, ensure_ascii=False)
    response_json = json.loads(result_json, encoding="utf-8")
    oper.log(response_json)
    try:
        send_msg.send_mail(result=response_json)
    except Exception as e:
        oper.log("发送邮件失败：" + str(e), 2)
    try:
        SoaClient.back_mq(response_json)
    except Exception as e:
        oper.log("返回队列信息失败：" + str(e), 2)
    try:
        SoaClient.del_mq(res)
    except Exception as e:
        oper.log("删除队列信息失败：" + str(e), 2)
    try:
        res_body = json.loads(res['msg_body'])
        base_info = res_body['base_info']
        read_files.del_apk(str(device_name) + '/' + base_info['app'])
    except Exception as e:
        oper.log("删除本地apk失败：" + str(e), 2)


def test_run(port, device_name):
    while True:
        res = SoaClient.get_mq()
        if res and res["msg_body"]:
            run_mq(res, port, device_name)
        else:
            time.sleep(1)


if __name__ == '__main__':
    test_run(4723, "127.0.0.1:62025")
    # print(run_xml.__doc__)
    # read_linux("caseUI\\/test\\/11.xml")
    # run_xml("caseUI\\/test\\/XianShiQiangGou.xml")
    # values = SaveValue()
    # values.save_value("name", "别闹")
    # value = values.get_value("name")
    # print(value)
    # values = SaveValue()
    # value = values.get_value("name")
    # print(value)
