#!/usr/bin/env python
# -*- coding:UTF-8 -*-
# 各模块链接
import pytest
import sys
import os

project_folder = os.getcwd()[0:os.getcwd().find("ui_auto_test")]
sys.path.append(project_folder + "ui_auto_test\\src")
sys.path.append(project_folder + "ui_auto_test\\src\\touch")
import helper
import oper


def test_func():
    helper.initial_appium(2)
    oper.switch_to_webview()
    page_resource = oper.get_page_resource()
    print(page_resource)
    oper.click("x,/html/body/div[2]/div/div[1]/ul/li[2]/a")
    oper.switch_to_native()
    oper.click("n,立即购买")


if __name__ == '__main__':
    try:
        test_func()
    except Exception as e:
        print(e)
    helper.release_appium()
