#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import find
import helper
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from logger import logger
from selenium.common.exceptions import WebDriverException
import requests
import check
import time
import re


def clear(element):
    """
    清空输入框的内容
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'

    """
    # 判断元素是否存在
    check.assert_exist_element(element)
    if isinstance(element, str):
        find.element(element).clear()
    else:
        element.clear()


def send_keys(element, text):
    """
    某个元素输入文本值
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        text: 输入的值
    """
    # 判断元素是否存在
    check.assert_exist_element(element)
    try:
        if isinstance(element, str):
            # find.element(element).clear()
            find.element(element).send_keys(text)
        else:
            # element.clear()
            element.send_keys(text)
    except Exception as e:
        # 下拉列表的输入框进行clear动作时会报异常，无法进行清空动作
        print(e)
        print("这个输入框不能进行清空动作")
        raise e


def click(element):
    """
    点击某个元素
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'

    """
    # 判断元素是否存在再点击
    check.assert_exist_element(element)
    if isinstance(element, str):
        find.element(element).click()
    else:
        element.click()


def driver_wait_click(element):
    """
    显示等待点击某元素
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'

    """
    if isinstance(element, str):
        find.element(element, 1).click()
    else:
        element.click()


def continuous_click(element, number, times=0):
    """
    连续点击某元素
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        number: 点击次数
        times: 每次时间间隔

    """
    for i in range(int(number)):
        click(element)
        if times:
            time.sleep(int(times))


def get_text(element):
    """
    获取某个元素的文本内容
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'

    Returns:
        元素定位的文本

    """
    # 判断元素是否存在
    check.assert_exist_element(element)
    if isinstance(element, str):
        return str(find.element(element).text)
    else:
        return element.text


def driver_wait_get_text(element):
    """
    显示等待某个元素的文本内容
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'

    Returns:
        元素定位的文本

    """
    if isinstance(element, str):
        return str(find.element(element, 1).text)
    else:
        return element.text


def get_attr(element, attribute):
    """
    获取元素的某个属性值
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        attribute: 属性，如'name'

    Returns:
        属性值
    """
    # 判断元素是否存在
    check.assert_exist_element(element)
    if isinstance(element, str):
        return find.element(element).get_attribute(attribute)
    else:
        return element.get_attribute(attribute)


def driver_wait_get_attr(element, attribute):
    """
    显示等待获取元素的某个属性值
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        attribute: 属性，如'name'

    Returns:
        属性值
    """
    if isinstance(element, str):
        return find.element(element, 1).get_attribute(attribute)
    else:
        return element.get_attribute(attribute)


def action_tap(element=None, x=None, y=None, count=1):
    """
    手势动作，点击某处
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        x: x轴相对位置
        y: y轴相对位置
        count: 点击次数, 默认一次
    Returns:
        点击动作
    """
    if x:
        x = float(x)
        y = float(y)
        window_size = get_size()
        x1 = int(window_size[0] * x)  # x坐标
        y1 = int(window_size[1] * y)  # 起始y坐标
        return TouchAction(helper.get_appium()).tap(x=x1, y=y1, count=count).release().perform()
    elif element:
        elements = find.element(element)
        return TouchAction(helper.get_appium()).tap(element=elements, count=count).release().perform()
    else:
        log("手势动作，点击某处，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，点击某处，传入参数错误无法实现操作！")


def action_press(element=None, x=None, y=None):
    """
    手势动作，按
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        x: x轴相对位置
        y: y轴相对位置

    Returns:
        手势动作，按
    """
    if x:
        x = float(x)
        y = float(y)
        window_size = get_size()
        x1 = int(window_size[0] * x)  # x坐标
        y1 = int(window_size[1] * y)  # 起始y坐标
        return TouchAction(helper.get_appium()).press(x=x1, y=y1).release().perform()
    elif element:
        elements = find.element(element)
        return TouchAction(helper.get_appium()).press(el=elements).release().perform()
    else:
        log("手势动作，按，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，按，传入参数错误无法实现操作！")


# 手势动作，释放
def action_release():
    return TouchAction(helper.get_appium()).release().perform()


def action_move_to(element=None, x=None, y=None):
    """
    手势动作，移动到
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        x: x轴相对位置
        y: y轴相对位置

    Returns:
        手势动作，移动到

    """
    if x:
        x = float(x)
        y = float(y)
        window_size = get_size()
        x1 = int(window_size[0] * x)  # x坐标
        y1 = int(window_size[1] * y)  # 起始y坐标
        return TouchAction(helper.get_appium()).move_to(x=x1, y=y1).release().perform()
    elif element:
        elements = find.element(element)
        return TouchAction(helper.get_appium()).move_to(el=elements).release().perform()
    else:
        log("手势动作，移动到，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，移动到，传入参数错误无法实现操作！")


def action_long_press(element=None, x=None, y=None, duration=1000):
    """
    手势动作，长按, 默认长按1秒钟
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        x: x轴相对位置
        y: y轴相对位置
        duration: 长按时间，默认长按1秒钟

    Returns:
        手势动作，长按
    """
    if x:
        x = float(x)
        y = float(y)
        window_size = get_size()
        x1 = int(window_size[0] * x)  # x坐标
        y1 = int(window_size[1] * y)  # 起始y坐标
        return TouchAction(helper.get_appium()).long_press(x=x1, y=y1, duration=duration).release().perform()
    elif element:
        elements = find.element(element)
        return TouchAction(helper.get_appium()).long_press(el=elements, duration=duration).release().perform()
    else:
        log("手势动作，长按，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，长按，传入参数错误无法实现操作！")


# 手势动作，动作完成发送至应用程序
def action_perform():
    return TouchAction(helper.get_appium()).perform()


# 手势动作，等待, 默认1s
def action_wait(ms=1000):
    return TouchAction(helper.get_appium()).wait(ms)


def action_slither(x1=None, y1=None, x2=None, y2=None, el1=None, el2=None):
    """
    手势动作，滑动x1y1 为起始坐标，x2y2为偏移坐标
    Args:
        x1: x1轴相对位置
        y1: y1轴相对位置
        x2: x2轴相对位置
        y2: y2轴相对位置
        el1: 对象1
        el2: 对象2

    Returns:
      手势动作，滑动
    """
    if x1:
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)
        window_size = get_size()
        x_1 = int(window_size[0] * x1)  # x1坐标
        y_1 = int(window_size[1] * y1)  # 起始y1坐标
        x_2 = int(window_size[0] * x2)  # x2坐标
        y_2 = int(window_size[1] * y2)  # 起始y2坐标
        return helper.get_appium().swipe(x_1, y_1, x_2, y_2)
        # return TouchAction(helper.get_appium()).press(x=x_1, y=y_1).move_to(x=x_2, y=y_2).release().perform()
    elif el1:
        element1 = find.element(el1)
        element2 = find.element(el2)
        return TouchAction(helper.get_appium()).press(element1).move_to(element2).release().perform()
    else:
        log("手势动作，滑动，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，滑动，传入参数错误无法实现操作！")


def action_multi(x1=None, y1=None, x2=None, y2=None, el1=None, el2=None):
    """
    多点触摸，两个手指触摸
    Args:
        x1: x1轴相对位置
        y1: y1轴相对位置
        x2: x2轴相对位置
        y2: y2轴相对位置
        el1: 对象1
        el2: 对象2

    Returns:
      多点触摸
    """
    if x1:
        x1 = float(x1)
        y1 = float(y1)
        x2 = float(x2)
        y2 = float(y2)
        window_size = get_size()
        x_1 = int(window_size[0] * x1)  # x1坐标
        y_1 = int(window_size[1] * y1)  # 起始y1坐标
        x_2 = int(window_size[0] * x2)  # x2坐标
        y_2 = int(window_size[1] * y2)  # 起始y2坐标
        action1 = TouchAction(helper.get_appium()).press(x=x_1, y=y_1)
        action2 = TouchAction(helper.get_appium()).press(x=x_2, y=y_2)
        ma = MultiAction(helper.get_appium())
        ma.add(action1, action2)
        ma.perform()
    elif el1:
        element1 = find.element(el1)
        element2 = find.element(el2)
        action1 = TouchAction(helper.get_appium()).tap(element1)
        action2 = TouchAction(helper.get_appium()).tap(element2)
        ma = MultiAction(helper.get_appium())
        ma.add(action1, action2)
        ma.perform()
    else:
        log("手势动作，多点触摸，传入参数错误无法实现操作！", 2)
        raise check.TouchException("手势动作，滑动，传入参数错误无法实现操作！")


# 向下滚动,execute_script()调用js
def rolling_down():
    return helper.get_appium().execute_script("mobile: scroll", {"direction": "down"})


def rolling_element(element, attr):
    """
    向元素的方向滚动
    Args:
        element: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        attr: 属性，如'name'

    Returns:
        向元素的方向滚动
    """
    return helper.get_appium().execute_script("mobile: scroll", {
        "direction": "down", "element": get_attr(element, attr)})


# 针对滑块 value “0.1”是10％，“1.0”是100％,xpath="//window[1]/slider[1]"
def action_slider(xpath, value):
    """
    针对滑块
    Args:
        xpath: 元素定位，如'x,//window[1]/slider[1]'
        value: “0.1”是10％，“1.0”是100％

    Returns:
        滑动
    """
    slider = find.element(xpath)
    return slider.send_keys(value)


def log(message, set_level=1, formats=None):
    """
    日志和控制台信息
    Args:
        message: 信息内容
        set_level: 默认值为1，不是1时给出error级别日志
        formats: 信息格式
    Returns:
        日志信息
    """
    if not formats:
        prefix = "- | - | - | - | "
    else:
        prefix = formats
    if set_level == 1:
        logger.info(str(prefix) + str(message))
        # print(message)
    else:
        logger.error(str(prefix) + str(message))
        # print("》》》》》" + str(message))


# 隐藏物理键盘操作
def hide_keyboard():
    try:
        helper.get_appium().hide_keyboard()
    except WebDriverException:
        return True
    else:
        return True


# 物理按键事件,常用返回键4，home键3，菜单键84
# https://www.cnblogs.com/feifei-cyj/p/8006780.html
def key_event(event):
    return helper.get_appium().keyevent(event)


class KeyEvent(object):
    def __init__(self, event_str):
        """

        Args:
            event_str: 物理键盘事件
            # KEYCODE列表
            # 电话键
            #  KEYCODE_CALL 拨号键
            #  KEYCODE_ENDCALL 挂机键
            #  KEYCODE_HOME 按键Home
            #  KEYCODE_MENU 菜单键
            #  KEYCODE_BACK 返回键
            #  KEYCODE_SEARCH 搜索键
            #  KEYCODE_CAMERA 拍照键
            #  KEYCODE_FOCUS 拍照对焦键
            #  KEYCODE_POWER 电源键
            #  KEYCODE_NOTIFICATION 通知键
            #  KEYCODE_MUTE 话筒静音键
            #  KEYCODE_VOLUME_MUTE 扬声器静音键
            #  KEYCODE_VOLUME_UP 音量增加键
            #  KEYCODE_VOLUME_DOWN 音量减小键
            # 控制键
            #  KEYCODE_ENTER 回车键
            #  KEYCODE_ESCAPE ESC键
            #  KEYCODE_DPAD_CENTER 导航键 确定键
            #  KEYCODE_DPAD_UP 导航键 向上
            #  KEYCODE_DPAD_DOWN 导航键 向下
            #  KEYCODE_DPAD_LEFT 导航键 向左
            #  KEYCODE_DPAD_RIGHT 导航键 向右
            #  KEYCODE_MOVE_HOME 光标移动到开始键
            #  KEYCODE_MOVE_END 光标移动到末尾键
            #  KEYCODE_PAGE_UP 向上翻页键
            #  KEYCODE_PAGE_DOWN 向下翻页键
            #  KEYCODE_DEL 退格键
            #  KEYCODE_FORWARD_DEL 删除键
            #  KEYCODE_INSERT 插入键
            #  KEYCODE_TAB Tab键
            #  KEYCODE_NUM_LOCK 小键盘锁
            #  KEYCODE_CAPS_LOCK 大写锁定键
            #  KEYCODE_BREAK Break/Pause键
            #  KEYCODE_SCROLL_LOCK 滚动锁定键
            #  KEYCODE_ZOOM_IN 放大键
            #  KEYCODE_ZOOM_OUT 缩小键
            # 组合键
            #  KEYCODE_ALT_LEFT Alt+Left
            #  KEYCODE_ALT_RIGHT Alt+Right
            #  KEYCODE_CTRL_LEFT Control+Left
            #  KEYCODE_CTRL_RIGHT Control+Right
            #  KEYCODE_SHIFT_LEFT Shift+Left
            #  KEYCODE_SHIFT_RIGHT Shift+Right
            # 基本键
            #  KEYCODE_0 按键'0'
            #  KEYCODE_1 按键'1'
            #  KEYCODE_2 按键'2'
            #  KEYCODE_3 按键'3'
            #  KEYCODE_4 按键'4'
            #  KEYCODE_5 按键'5'
            #  KEYCODE_6 按键'6'
            #  KEYCODE_7 按键'7'
            #  KEYCODE_8 按键'8'
            #  KEYCODE_9 按键'9'
            #  KEYCODE_A 按键'A'
            #  KEYCODE_B 按键'B'
            #  KEYCODE_C 按键'C'
            #  KEYCODE_D 按键'D'
            #  KEYCODE_E 按键'E'
            #  KEYCODE_F 按键'F'
            #  KEYCODE_G 按键'G'
            #  KEYCODE_H 按键'H'
            #  KEYCODE_I 按键'I'
            #  KEYCODE_J 按键'J'
            #  KEYCODE_K 按键'K'
            #  KEYCODE_L 按键'L'
            #  KEYCODE_M 按键'M'
            #  KEYCODE_N 按键'N'
            #  KEYCODE_O 按键'O'
            #  KEYCODE_P 按键'P'
            #  KEYCODE_Q 按键'Q'
            #  KEYCODE_R 按键'R'
            #  KEYCODE_S 按键'S'
            #  KEYCODE_T 按键'T'
            #  KEYCODE_U 按键'U'
            #  KEYCODE_V 按键'V'
            #  KEYCODE_W 按键'W'
            #  KEYCODE_X 按键'X'
            #  KEYCODE_Y 按键'Y'
            #  KEYCODE_Z 按键'Z'
            # 符号键
            #  KEYCODE_PLUS 按键'+'
            #  KEYCODE_MINUS 按键'-'
            #  KEYCODE_STAR 按键'*'
            #  KEYCODE_SLASH 按键'/'
            #  KEYCODE_EQUALS 按键'='
            #  KEYCODE_AT 按键'@'
            #  KEYCODE_POUND 按键'#'
            #  KEYCODE_APOSTROPHE 按键(单引号)
            #  KEYCODE_BACKSLASH 按键'\'
            #  KEYCODE_COMMA 按键','
            #  KEYCODE_PERIOD 按键'.'
            #  KEYCODE_LEFT_BRACKET 按键'['
            #  KEYCODE_RIGHT_BRACKET 按键']'
            #  KEYCODE_SEMICOLON 按键';'
            #  KEYCODE_GRAVE 按键'`'
            #  KEYCODE_SPACE 空格键
        """
        self.arguments = {
            '0': 7, '1': 8, '2': 9, '3': 10, '4': 11, '5': 12, '6': 13, '7': 14, '8': 15, '9': 16, 'A': 29, 'B': 30,
            'C': 31, 'D': 32, 'E': 33, 'F': 34, 'G': 35, 'H': 36, 'I': 37, 'J': 38, 'K': 39, 'L': 40, 'M': 41, 'N': 42,
            'O': 43, 'P': 44, 'Q': 45, 'R': 46, 'S': 47, 'T': 48, 'U': 49, 'V': 50, 'W': 51, 'X': 52, 'Y': 53, 'Z': 54,
            '+': 81, '-': 69, '*': 17, '/': 76, '=': 70, '@': 77, '#': 18, "'": 75, "\\": 73, ',': 55, '.': 56, '[': 71,
            ']': 72, ';': 74, '`': 68, ' ': 62
        }
        self.key_code = {
            'KEYCODE_CALL': 5, 'KEYCODE_ENDCALL': 6, 'KEYCODE_HOME': 3, 'KEYCODE_MENU': 82, 'KEYCODE_BACK': 4,
            'KEYCODE_SEARCH': 84, 'KEYCODE_CAMERA': 27, 'FOCUS': 80, 'KEYCODE_POWER': 26, 'KEYCODE_NOTIFICATION': 83,
            'KEYCODE_MUTE': 91, 'KEYCODE_VOLUME_MUTE': 164, 'KEYCODE_VOLUME_UP': 24, 'KEYCODE_VOLUME_DOWN': 25,
            'KEYCODE_ENTER': 66, 'KEYCODE_ESCAPE': 111, 'KEYCODE_DPAD_CENTER': 23, 'KEYCODE_DPAD_UP': 19,
            'KEYCODE_DPAD_DOWN': 20, 'KEYCODE_DPAD_LEFT': 21, 'KEYCODE_DPAD_RIGHT': 22, 'KEYCODE_MOVE_HOME': 122,
            'KEYCODE_MOVE_END': 123, 'KEYCODE_PAGE_UP': 92, 'KEYCODE_PAGE_DOWN': 93, 'KEYCODE_DEL': 67,
            'KEYCODE_FORWARD_DEL': 112, 'KEYCODE_INSERT': 124, 'KEYCODE_TAB': 61, 'KEYCODE_NUM_LOCK': 143,
            'KEYCODE_CAPS_LOCK': 115, 'KEYCODE_BREAK': 121, 'KEYCODE_SCROLL_LOCK': 116, 'KEYCODE_ZOOM_IN': 168,
            'KEYCODE_ZOOM_OUT': 169, 'KEYCODE_ALT_LEFT': 57, 'KEYCODE_ALT_RIGHT': 58, 'KEYCODE_CTRL_LEFT': 113,
            'KEYCODE_CTRL_RIGHT': 114, 'KEYCODE_SHIFT_LEFT': 59, 'KEYCODE_SHIFT_RIGHT': 60, 'KEYCODE_0': 7,
            'KEYCODE_1': 8, 'KEYCODE_2': 9, 'KEYCODE_3': 10, 'KEYCODE_4': 11, 'KEYCODE_5': 12, 'KEYCODE_6': 13,
            'KEYCODE_7': 14, 'KEYCODE_8': 15, 'KEYCODE_9': 16, 'KEYCODE_A': 29, 'KEYCODE_B': 30,
            'KEYCODE_C': 31, 'KEYCODE_D': 32, 'KEYCODE_E': 33, 'KEYCODE_F': 34, 'KEYCODE_G': 35, 'KEYCODE_H': 36,
            'KEYCODE_I': 37, 'KEYCODE_J': 38, 'KEYCODE_K': 39, 'KEYCODE_L': 40, 'KEYCODE_M': 41, 'KEYCODE_N': 42,
            'KEYCODE_O': 43, 'KEYCODE_P': 44, 'KEYCODE_Q': 45, 'KEYCODE_R': 46, 'KEYCODE_S': 47, 'KEYCODE_T': 48,
            'KEYCODE_U': 49, 'KEYCODE_V': 50, 'KEYCODE_W': 51, 'KEYCODE_X': 52, 'KEYCODE_Y': 53, 'KEYCODE_Z': 54,
            'KEYCODE_PLUS': 81, 'KEYCODE_MINUS': 69, 'KEYCODE_STAR': 17, 'KEYCODE_SLASH': 76, 'KEYCODE_EQUALS': 70,
            'KEYCODE_AT': 77, 'KEYCODE_POUND': 18, 'KEYCODE_APOSTROPHE': 75, 'KEYCODE_BACKSLASH': 73,
            'KEYCODE_COMMA': 55, 'KEYCODE_PERIOD': 56, 'KEYCODE_LEFT_BRACKET': 71, 'KEYCODE_RIGHT_BRACKET': 72,
            'KEYCODE_SEMICOLON': 74, 'KEYCODE_GRAVE': 68, 'KEYCODE_SPACE': 62,
        }
        self.event_str = event_str

    # 单一事件，后续可能存在组合事件
    def event(self):
        if 'KEYCODE' in self.event_str:
            KeyEvent.key_code(self)
        else:
            KeyEvent.arguments(self)

    @staticmethod
    def key_code(self):
        for key, value in self.key_code.items():
            if self.event_str.upper() in self.key_code.keys():
                if key.lower() == self.event_str.lower():
                    key_event(value)
                    break
            else:
                log("物理按键键值不合法，请排查", 2)

    @staticmethod
    def arguments(self):
        for i in self.event_str:
            for key, value in self.arguments.items():
                if key.lower() == i.lower():
                    key_event(value)


# 获得机器屏幕大小x,y
def get_size():
    x = helper.get_appium().get_window_size()['width']
    y = helper.get_appium().get_window_size()['height']
    size = (x, y)
    return size


# 屏幕向上滑动，t等待ms，location
def swipe_up(loc=0.5, t=None):
    loc = float(loc)
    window_size = get_size()
    x1 = int(window_size[0] * loc)  # x坐标
    y1 = int(window_size[1] * 0.5)  # 起始y坐标
    y2 = int(window_size[1] * 0.25)  # 终点y坐标
    return helper.get_appium().swipe(x1, y1, x1, y2, t)


# 屏幕向下滑动，t等待ms
def swipe_down(loc=0.5, t=None):
    loc = float(loc)
    window_size = get_size()
    x1 = int(window_size[0] * loc)  # x坐标
    y1 = int(window_size[1] * 0.25)  # 起始y坐标
    y2 = int(window_size[1] * 0.75)  # 终点y坐标
    helper.get_appium().swipe(x1, y1, x1, y2, t)


# 屏幕向左滑动，t等待ms
def swipe_left(loc=0.5, t=None):
    loc = float(loc)
    window_size = get_size()
    x1 = int(window_size[0] * 0.75)
    y1 = int(window_size[1] * loc)
    x2 = int(window_size[0] * 0.05)
    helper.get_appium().swipe(x1, y1, x2, y1, t)


# 屏幕向右滑动，t等待ms
def swipe_right(loc=0.5, t=None):
    loc = float(loc)
    window_size = get_size()
    x1 = int(window_size[0] * 0.05)
    y1 = int(window_size[1] * loc)
    x2 = int(window_size[0] * 0.75)
    helper.get_appium().swipe(x1, y1, x2, y1, t)


def get_current_context():
    """
    获取当前页面的webview名
    :return:
    """
    contexts = []
    for i in range(10):
        contexts = helper.get_appium().contexts
        log(contexts)
        time.sleep(1)
        if len(contexts) > 1:
            break
    if len(contexts) > 1:
        return contexts[1]
    else:
        log("当前页面不存在webview名！", 2)
        raise check.TouchException("当前页面不存在webview名！")


def switch_to_webview():
    """
    切换到webview
    """
    current_context = get_current_context()
    try:
        helper.get_appium().switch_to.context(current_context)
        current_context = helper.get_appium().current_context
        log("已切换webview到：" + str(current_context))
    except Exception as e:
        log("切换webview为" + str(current_context) + "失败，原因是" + str(e), 2)
        raise check.TouchException("切换webview为" + str(current_context) + "失败，原因是" + str(e))


def switch_to_native():
    """
    切换到原生页面
    """
    try:
        helper.get_appium().switch_to.context("NATIVE_APP")
        current_context = helper.get_appium().current_context
        log("已切换到原生：" + str(current_context))
    except Exception as e:
        log("切换回原生页面失败，原因是" + str(e), 2)
        raise check.TouchException("切换回原生页面失败，原因是" + str(e))


def get_page_resource():
    """
    获取当前页面资源（页面元素）
    :return: 整个页面元素
    """
    page_source = helper.get_appium().page_source
    log(page_source)
    return page_source


def download_apk(f):
    """
    下载apk
    Args:
        f:apk名称
    Returns:

    """
    url = helper.read_config_item("apk", "url") + f
    filename = helper.srcPath + '/common/' + f
    file = requests.get(url, timeout=10)
    with open(filename, 'wb') as apk:
        apk.write(file.content)
        log("下载" + f + "成功")
    # 返回内容
    dicts = [url, 'Succeed', filename]
    return dicts


class CalStyle(object):

    def add(self, value_1, value_2):
        """
        加法
        """
        # value_1 = float(value_1)
        # value_2 = float(value_2)
        # result = "%.2f" % float(value_1 + value_2)
        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            result = "%.2f" % float(value_1 + value_2)
        else:
            result = str(value_1 + value_2)
        return result

    def sub(self, value_1, value_2):
        """
        减法
        """
        # value_1 = float(value_1)
        # value_2 = float(value_2)
        # result = "%.2f" % float(value_1 - value_2)
        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            result = "%.2f" % float(value_1 - value_2)
        else:
            result = str(value_1 - value_2)
        return result

    def mul(self, value_1, value_2):
        """
        乘法
        """
        # value_1 = float(value_1)
        # value_2 = float(value_2)
        # result = "%.2f" % float(value_1 * value_2)
        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            result = "%.2f" % float(value_1 * value_2)
        else:
            result = str(value_1 * value_2)
        return result

    def div(self, value_1, value_2):
        """
        除法
        """
        # value_1 = float(value_1)
        # value_2 = float(value_2)
        # result = "%.2f" % float(value_1 / value_2)
        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            result = "%.2f" % float(value_1 / value_2)
        else:
            result = str(value_1 / value_2)
        return result

    def equal(self, value_1, value_2):
        """
        等于
        """

        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            value_1 = "%.2f" % float(value_1)
            value_2 = "%.2f" % float(value_2)
        check.compare(value_1, value_2)

    def notequal(self, value_1, value_2):
        """
        不等于
        """
        # value_1 = "%.2f" % float(value_1)
        # value_2 = "%.2f" % float(value_2)
        value_1, value_2 = self.dispose_number(value_1, value_2)
        if isinstance(value_1, float) or isinstance(value_2, float):
            value_1 = "%.2f" % float(value_1)
            value_2 = "%.2f" % float(value_2)
        check.compare_not(value_1, value_2)

    def greater_than(self, value_1, value_2):
        """
        大于
        """
        value_1, value_2 = self.dispose_number(value_1, value_2)
        check.compare_than(value_1, value_2, "大于")

    def greater_than_equal(self, value_1, value_2):
        """
        大于等于
        """
        value_1, value_2 = self.dispose_number(value_1, value_2)
        check.compare_than(value_1, value_2, "大于等于")

    def less_than(self, value_1, value_2):
        """
        小于
        """
        value_1, value_2 = self.dispose_number(value_1, value_2)
        check.compare_than(value_1, value_2, "小于")

    def less_than_equal(self, value_1, value_2):
        """
        小于等于
        """
        value_1, value_2 = self.dispose_number(value_1, value_2)
        check.compare_than(value_1, value_2, "小于等于")

    def dispose_number(self, value_1, value_2):
        """
        针对不同数据给出不同数据类型
        :param value_1: 数据1
        :param value_2: 数据2
        :return:
        对应的数据int或者float
        """
        if "." in value_1:
            value_list_1 = str(value_1).split('.')
            str_1 = value_list_1[0]
            str_2 = value_list_1[1]
            num_1 = self.get_str_to_num(str_1)
            num_2 = self.get_str_to_num(str_2)
            cal_num_1 = num_1 + '.' + num_2
        else:
            cal_num_1 = self.get_str_to_num(value_1)
        if "." in value_2:
            value_list_2 = str(value_2).split('.')
            str_1 = value_list_2[0]
            str_2 = value_list_2[1]
            num_1 = self.get_str_to_num(str_1)
            num_2 = self.get_str_to_num(str_2)
            cal_num_2 = num_1 + '.' + num_2
        else:
            cal_num_2 = self.get_str_to_num(value_2)
        if "." in cal_num_1 or "." in cal_num_2:
            cal_num_1 = float(cal_num_1)
            cal_num_2 = float(cal_num_2)
        else:
            cal_num_1 = int(cal_num_1)
            cal_num_2 = int(cal_num_2)
        return cal_num_1, cal_num_2

    @staticmethod
    def get_str_to_num(string):
        """
        字符换中提取数值
        :param string: 字符串
        :return:
        匹配到的数值,数据类型str
        """
        values = re.sub("\D", "", string)
        if not values:
            values = "0"
        return values


if __name__ == '__main__':
    three = CalStyle().add("0", "5.0")
    CalStyle().equal(three, "5.0w")
    # CalStyle().greater_than("鲜花:24", "鲜花:3.5")
    # CalStyle().greater_than_equal("鲜花:24", "鲜花:3.5")
    # CalStyle().less_than("鲜花:24", "鲜花:35")
    # CalStyle().less_than_equal("鲜花:24", "鲜花:35")
    # num_value = CalStyle().add("鲜花:24", "鲜花:3.5")
    # num_value_2 = CalStyle().sub("鲜花:24", "鲜花:3.5")
    # num_value_3 = CalStyle().mul("鲜花:24", "鲜花:3.5")
    # num_value_4 = CalStyle().div("鲜花:24", "鲜花:3.5")
    # CalStyle().notequal("鲜花:24", "鲜花:3.5")
    # CalStyle().equal("24.0", "24")
    # print(num_value)
