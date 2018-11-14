#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import check
import oper


# 清理环境
def clean():
    try:
        clean_init()
        clean_window()
    except Exception as e:
        oper.log("清理失败" + str(e))
    return True


# 清理初始页
def clean_init():
    try:
        check.wait_element("i,com.xingjiabi.shengsheng:id/tvGuideLogin")
        check.exist_element("i,com.xingjiabi.shengsheng:id/tvGuideLogin")
        oper.driver_wait_click("i,com.xingjiabi.shengsheng:id/tvGuideLogin")
        oper.action_press(x=0.5, y=0.95)
        check.wait_element("n,请选择性别")
        check.exist_element("n,请选择性别")
        oper.click("i,com.xingjiabi.shengsheng:id/ivSwitchGenderMan")
    except Exception as e:
        oper.log("清理初始化页面失败：" + str(e), 2)


# 清理商城弹窗
def clean_window():
    try:
        check.wait_element("n,商城")
        oper.click("n,商城")
        check.wait_element("i,com.xingjiabi.shengsheng:id/ivClose")
        oper.click("i,com.xingjiabi.shengsheng:id/ivClose")
        check.wait_element("n,我")
    except Exception as e:
        oper.log("清理弹窗页面失败：" + str(e), 2)


if __name__ == '__main__':
    clean()
