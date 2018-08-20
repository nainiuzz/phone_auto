#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import check
import oper
from logger import logger
import find
import time
import helper


# 登录
def login(phone=helper.read_config_item("account_info", "phone"),
          password=helper.read_config_item("account_info", "password"),
          name=helper.read_config_item("account_info", "name")):
    """
    登录操作
    Args:
        phone: 电话号码，默认值配置文件的account_info的phone
        password: 密码，默认值配置文件的account_info的password
        name: 用户名，默认值配置文件的account_info的name
    Returns:
        True
    """
    check.wait_element("x,//android.widget.TabWidget/android.widget.RelativeLayout[5]/android.widget.ImageView[1]")
    if check.exist_element("x,//android.widget.TabWidget/android.widget.RelativeLayout[5]/android.widget.ImageView[1]"):
        elem = find.element("x,//android.widget.TabWidget/android.widget.RelativeLayout[5]/android.widget.ImageView[1]")
        oper.action_tap(elem)
        oper.click("x,//android.widget.TabWidget/android.widget.RelativeLayout[5]/android.widget.ImageView[1]")
        check.wait_element("i,com.xingjiabi.shengsheng:id/btnLogin", 5)
        if check.exist_element("i,com.xingjiabi.shengsheng:id/btnLogin"):
            logger.info("现在处于未登录状态")
            oper.click("i,com.xingjiabi.shengsheng:id/btnLogin")
            check.wait_element("i,com.xingjiabi.shengsheng:id/xjb_login_name")
            login_action(phone, password, name)
        elif check.exist_element("i,com.xingjiabi.shengsheng:id/tvAccountName"):
            user_name = oper.get_text("i,com.xingjiabi.shengsheng:id/tvAccountName")
            if name == user_name:
                logger.info("已正确登录")
            else:
                logout()
                login_action(phone, password, name)
        else:
            logger.error("》》》》》进入登录界面失败")
            raise check.TouchException("》》》》》登录失败")
    return True


# 退出登录
def logout():
    if check.exist_element("i,com.xingjiabi.shengsheng:id/tvTopRight"):
        oper.click("i,com.xingjiabi.shengsheng:id/tvTopRight")
        check.wait_text("设置")
        oper.swipe_up()
        check.wait_element("i,com.xingjiabi.shengsheng:id/login_off_layout")
        if check.exist_element("i,com.xingjiabi.shengsheng:id/login_off_layout"):
            oper.click("i,com.xingjiabi.shengsheng:id/login_off_layout")
            check.wait_element("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive")
            if check.exist_element("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive"):
                oper.click("i,com.xingjiabi.shengsheng:id/md_buttonDefaultPositive")
                check.wait_element_disappear("i,com.xingjiabi.shengsheng:id/login_off_layout")
                if not check.exist_element("i,com.xingjiabi.shengsheng:id/login_off_layout"):
                    logger.info("退出成功")
                else:
                    oper.log("退出失败", 2)
            else:
                oper.log("无退出登录确认弹窗", 2)
        else:
            oper.log("不存在【退出登录】按钮，无法执行退出操作", 2)
    else:
        print("当前不处于他趣系统登陆界面，无法进行退出动作")
    time.sleep(2)


# 登录动作
def login_action(phone, password, name):
    """
    登录动作
    Args:
        phone: 电话号码，默认值配置文件的account_info的phone
        password: 密码，默认值配置文件的account_info的password
        name: 用户名，默认值配置文件的account_info的name
    """
    if check.exist_element("i,com.xingjiabi.shengsheng:id/xjb_login_name"):
        oper.send_keys("i,com.xingjiabi.shengsheng:id/xjb_login_name", phone)
        if check.exist_element("i,com.xingjiabi.shengsheng:id/xjb_login_psd"):
            oper.send_keys("i,com.xingjiabi.shengsheng:id/xjb_login_psd", password)
            # oper.hide_keyboard()
            if check.exist_element("i,com.xingjiabi.shengsheng:id/xjb_login_but"):
                oper.click("i,com.xingjiabi.shengsheng:id/xjb_login_but")
            else:
                oper.log("登录按钮被隐藏，无法点击", 2)
                raise check.TouchException("》》》》》登录按钮被隐藏，无法点击")
            check.wait_text(name)
            if check.exist_text(name):
                logger.info("登录成功")
                print("登录成功")
            else:
                logger.error("》》》》》登录失败")
                raise check.TouchException("》》》》》登录失败")
    return


if __name__ == '__main__':
    login()
