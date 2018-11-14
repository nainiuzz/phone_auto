#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import check
import oper
import helper
import SoaClient


# 登录
def login(phone, password=helper.read_config_item("account_info", "password")):
    """
    登录操作
    Args:
        phone: 电话号码，默认值配置文件的account_info的phone
        password: 密码，默认值配置文件的account_info的password
    Returns:
        True
    """
    check.wait_element("n,我")
    oper.click("n,我")
    check.wait_element("i,com.xingjiabi.shengsheng:id/btnUserLogin")
    oper.click("i,com.xingjiabi.shengsheng:id/btnUserLogin")
    check.wait_element("x,//android.widget.TextView[@resource-id='com.xingjiabi.shengsheng:id/tvXjbLoginTab']")
    oper.click("x,//android.widget.TextView[@resource-id='com.xingjiabi.shengsheng:id/tvXjbLoginTab']")
    check.wait_element("i,com.xingjiabi.shengsheng:id/xjb_login_name")
    oper.clear("i,com.xingjiabi.shengsheng:id/xjb_login_name")
    oper.send_keys("i,com.xingjiabi.shengsheng:id/xjb_login_name", phone)
    oper.clear("i,com.xingjiabi.shengsheng:id/xjb_login_psd")
    oper.send_keys("i,com.xingjiabi.shengsheng:id/xjb_login_psd", password)
    oper.click("i,com.xingjiabi.shengsheng:id/xjb_login_but")
    check.wait_element("n,我")
    check.assert_exist_element("n,我")


# 退出登录
def logout():
    check.wait_element("n,我")
    oper.click("n,我")
    check.wait_element("i,com.xingjiabi.shengsheng:id/ivMineToolbarSetting")
    oper.click("i,com.xingjiabi.shengsheng:id/ivMineToolbarSetting")
    check.wait_text("通用设置")
    oper.swipe_up()
    check.wait_element("i,com.xingjiabi.shengsheng:id/login_off_layout")
    oper.click("i,com.xingjiabi.shengsheng:id/login_off_layout")
    check.wait_element("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive")
    oper.click("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive")
    check.wait_element_disappear("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive")
    check.assert_not_exist_element("i,com.xingjiabi.shengsheng:id/mad_buttonDefaultPositive")
    # 退出设置模块
    check.wait_text("通用设置")
    check.assert_exist_text("通用设置")
    check.wait_element("i,com.xingjiabi.shengsheng:id/top_left_button")
    oper.click("i,com.xingjiabi.shengsheng:id/top_left_button")
    check.wait_element("n,我")
    check.assert_exist_element("n,我")


def login_read_xml(xml_path, port):
    """
    根据xml地址判断登录模拟器对应的哪个账号
    :param xml_path: xml地址
    :param port: 设备端口
    :return: 登录动作
    """
    device_str = ""
    login_value = oper.CalStyle().get_str_to_num(xml_path)
    pool = SoaClient.get_pool()
    for _pool in pool:
        if _pool['port'] == str(port):
            device_str = _pool['pool']
    device = device_str.split(",")
    # pool = helper.read_config_item("phone_pool")
    # device = pool[int(port) - 4723]
    if login_value == "0":
        phone = device[int(login_value)]
    else:
        phone = device[int(login_value) - 1]
    login(phone)


if __name__ == '__main__':
    login_read_xml("caseUI/Me/Login/Login2", 4724)
