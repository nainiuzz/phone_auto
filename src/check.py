#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import time
import find
import helper
import oper
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_element(element_sequence, timeout=10):
    """
    等待某个元素出现
    Args:
        element_sequence: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        timeout: 超时等待时间，默认10s

    Returns:
        True or False
    """

    def _wait_element():
        return exist_element(element_sequence)

    return handle_timeout(_wait_element, timeout)


def wait_element_disappear(element_sequence, timeout=10):
    """
    等待某个元素消失
    Args:
        element_sequence: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        timeout: 超时等待时间，默认10s

    Returns:
        True or False
    """

    def _wait_element_disappear():
        return not exist_element(element_sequence)

    return handle_timeout(_wait_element_disappear, timeout)


def wait_text(content, timeout=10):
    """
    等待某段文字出现
    Args:
        content: 文字，str
        timeout: 超时等待时间，默认10s

    Returns:
        True or False
    """

    def _wait_text():
        return exist_text(content)

    return handle_timeout(_wait_text, timeout)


def wait_text_disappear(content, timeout=10):
    """
    等待某段文字消失
    Args:
        content: 文字，str
        timeout: 超时等待时间，默认10s

    Returns:
        True or False
    """

    def _wait_text_disappear():
        return not exist_text(content)

    return handle_timeout(_wait_text_disappear, timeout)


def exist_element(element_sequence):
    """
    判断元素是否存在
    Args:
        element_sequence: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
    Returns:
        True or False
    """
    try:
        if find.element(element_sequence):
            return True
    except:
        return False


def displayed_element(element_sequence):
    """
    判断元素是否显示
    Args:
        element_sequence: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
    Returns:
        True or False
    """
    try:
        if find.element(element_sequence).is_displayed():
            return True
    except:
        return False


def exist_iframe(iframe=None):
    """
    判断页面是否存在iframe
    Args:
        iframe: frame的元素定位
    Returns:
        True or False
    """
    try:
        if not iframe:
            return find.element("t,iframe")
        else:
            return find.element(iframe)
    except:
        return False


def exist_text(content):
    """
    判断文字是否存在
    Args:
        content: 文字，str
    Returns:
        True or False
    """
    try:
        if find.element("n," + content).is_displayed():
            return True
    except:
        return False


def exist_toast(text, timeout=30, poll_frequency=0.5):
    """
    判断浮窗是否存在
    Args:
        text: 页面上看到的文本内容
        timeout: 最大超时时间，默认10s
        poll_frequency: 间隔查询时间，默认0.5s查询一次

    Returns:
        True or False

    """
    try:
        toast_loc = ("xpath", ".//*[contains(@text,'%s')]" % text)
        WebDriverWait(helper.get_appium(), timeout, poll_frequency).until(EC.presence_of_element_located(toast_loc))
        return True
    except:
        return False


def assert_exist_toast(text):
    """
    判断浮窗是否存在
    Args:
        text: 元素定位，str
    Returns:
        断言失败异常
    """
    if not exist_toast(text):
        oper.log(text + "该浮窗不存在", 2)
        raise TouchException(text + "该浮窗不存在")


def assert_not_exist_toast(text):
    """
    判断浮窗是否不存在
    Args:
        text: 元素定位，str
    Returns:
        断言失败异常
    """
    if exist_toast(text):
        oper.log(text + "该浮窗仍然存在", 2)
        raise TouchException(text + "该浮窗仍然存在")


def assert_exist_element(element_sequence):
    """
    判断文字是否存在
    Args:
        element_sequence: 元素定位，str
    Returns:
        断言失败异常
    """
    if not exist_element(element_sequence):
        oper.log(element_sequence + "该对象不存在", 2)
        raise TouchException(element_sequence + "该对象不存在")


def assert_not_exist_element(element_sequence):
    """
    判断文字是否存在
    Args:
        element_sequence: 元素定位，str
    Returns:
        断言失败异常
    """
    if exist_element(element_sequence):
        oper.log(element_sequence + "该对象仍然存在", 2)
        raise TouchException(element_sequence + "该对象仍然存在")


def assert_exist_text(content):
    """
       判断文字是否存在
       Args:
           content: 文字，str
       Returns:
           断言失败异常
       """
    if not exist_text(content):
        oper.log(content + "该文字不存在", 2)
        raise TouchException(content + "该文字不存在")


def assert_not_exist_text(content):
    """
       判断文字是否不存在
       Args:
           content: 文字，str
       Returns:
           断言失败异常
       """
    if exist_text(content):
        oper.log(content + "该文字仍然存在", 2)
        raise TouchException(content + "该文字仍然存在")


def wait_for_load(timeout=10):
    """
    等待页面加载标记消失
    Args:
        timeout: 超时等待时间，默认10s
    """
    wait_element_disappear("x,//*[@class='load']", timeout)
    wait_text_disappear("加载中...", timeout)
    wait_text_disappear("计算中...", timeout)


# 判断是否有页面异常出现，并尝试恢复动作
def handle_timeout(func, timeout=10, *args, **param_map):
    """
    判断是否有页面异常出现，并尝试恢复动作
    Args:
        func: 方法名
        timeout: 超时等待时间，默认10s
        *args: 非固定参数
        **param_map: 非固定参数
    Returns:

    """
    rst = None
    while timeout > 0:
        try:
            rst = func(*args, **param_map)
            if exist_text("系统繁忙 试试刷新页面"):
                rst = TouchException("系统繁忙 试试刷新页面")
                break
            elif exist_element("i,com.xingjiabi.shengsheng:id/tvErrorCode"):
                rst = TouchException(oper.get_text("i,com.xingjiabi.shengsheng:id/tvErrorCode"))
                break
            elif rst and not is_except(rst):
                break
        except:
            if rst and not is_except(rst):
                break
        time.sleep(1)
        timeout -= 1
    if is_except(rst):
        raise rst
    elif rst is None:
        raise TouchException("》》》》》方法没有返回值")
    elif rst:
        return rst


# 定义touch系统异常
class TouchException(Exception):
    print(Exception)
    pass


def is_except(e, e_type=Exception):
    return isinstance(e, e_type)


def compare(predicted_value, actual_value):
    """
    比较
    Args:
        predicted_value: 预期值
        actual_value: 实际值

    Returns:
        log信息

    """
    try:
        # 预计值predicted_value对比实际值actual_value
        assert str(predicted_value).replace(" ", "").replace("\n", "") == str(actual_value).replace(" ", "").replace(
            "\n", "")
        oper.log('校验成功。预计值:%s,实际值:%s' % (predicted_value, actual_value))
    except AssertionError:
        oper.log('》》》》》校验失败。预计值:%s,实际值:%s' % (predicted_value, actual_value), 2)
        raise TouchException('》》》》》校验失败。预计值:%s,实际值:%s' % (predicted_value, actual_value))


def compare_not(predicted_value, actual_value):
    """
    比较
    Args:
        predicted_value: 预期值
        actual_value: 实际值

    Returns:
        log信息

    """
    try:
        # 预计值predicted_value对比实际值actual_value
        assert str(predicted_value).replace(" ", "").replace("\n", "") != str(actual_value).replace(" ", "").replace(
            "\n", "")
        oper.log('校验成功。预计值:%s,实际值:%s' % (predicted_value, actual_value))
    except AssertionError:
        oper.log('》》》》》校验失败。预计值:%s,实际值:%s' % (predicted_value, actual_value), 2)
        raise TouchException('》》》》》校验失败。预计值:%s,实际值:%s' % (predicted_value, actual_value))


def compare_than(value_1, value_2, sign):
    """
    比较两个值大小
    :param value_1: 值1
    :param value_2: 值2
    :param sign: 触发不同的比较，如1.大于，2.大于等于，3.小于，4.小于等于
    :return:
        比较结果
    """
    try:
        if sign == "大于":
            assert value_1 > value_2
        elif sign == "大于等于":
            assert value_1 >= value_2
        elif sign == "小于":
            assert value_1 < value_2
        else:
            assert value_1 <= value_2
        oper.log('校验成功。%s是%s %s' % (value_1, sign, value_2))
    except AssertionError:
        oper.log('》》》》》校验失败。%s不是%s%s' % (value_1, sign, value_2), 2)
        raise TouchException('》》》》》校验失败。%s不是%s %s' % (value_1, sign, value_2))


# 用例执行结果校验
def case_check():
    flag = helper.read_config_item("flag", "compare_flag")
    assert flag == "0", "用例执行失败"


if __name__ == '__main__':
    wait_text('商城')
    print('商城')
