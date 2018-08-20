#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import helper
import check
import oper
from selenium.webdriver.support.wait import WebDriverWait


def element(selector, waits=None):
    """
    Args:
        selector: 元素定位，如'i,com.xingjiabi.shengsheng:id/btnLogin'
        waits: 显式等待标记，用于加载缓慢的元素定位
    Returns:

    """
    index = 0
    if ',' not in selector:
        return helper.get_appium().find_element_by_id(selector)
    selector_by = selector.split(',')[0]
    selector_value = selector.split(',')[1]
    if 's' in selector_by:
        if '[' in selector_value:
            selector_location = selector_value.split('[')[0]
            index = selector_value.split('[')[1].replace("]", "")
            selector_value = selector_location
    # selector_value = selector_value.replace(" ", "")

    try:
        if waits:
            wait_driver = WebDriverWait(helper.get_appium(), 30)
            if selector_by == "i" or selector_by == 'id':
                ele = wait_driver.until(lambda x: x.find_element_by_id(selector_value))
            elif selector_by == "n" or selector_by == 'name':
                ele = wait_driver.until(
                    lambda x: x.find_element_by_xpath("//*[@text='" + selector_value + "']"))
            elif selector_by == "c" or selector_by == 'class_name':
                ele = wait_driver.until(
                    lambda x: x.find_element_by_class_name(selector_value))
            elif selector_by == "l" or selector_by == 'link':
                ele = wait_driver.until(
                    lambda x: x.find_element_by_link_text(selector_value))
            elif selector_by == "p" or selector_by == 'partial_link_text':
                ele = wait_driver.until(
                    lambda x: x.find_element_by_partial_link_text(selector_value))
            elif selector_by == "t" or selector_by == 'tag_name':
                ele = wait_driver.until(lambda x: x.find_element_by_tag_name(selector_value))
            elif selector_by == "x" or selector_by == 'xpath':
                ele = wait_driver.until(lambda x: x.find_element_by_xpath(selector_value))
            elif selector_by == "a" or selector_by == 'android_uiautomator':
                ele = wait_driver.until(
                    lambda x: x.find_element_by_android_uiautomator(selector_value))
            elif selector_by == "is" or selector_by == 'ids':
                ele = wait_driver.until(lambda x: x.find_elements_by_id(selector_value)[int(index)])
            elif selector_by == "ns" or selector_by == 'names':
                ele = wait_driver.until(
                    lambda x: x.find_elements_by_xpath("//*[@text='" + selector_value + "']")[int(index)])
            elif selector_by == "cs" or selector_by == 'class_names':
                ele = wait_driver.until(
                    lambda x: x.find_elements_by_class_name(selector_value)[int(index)])
            elif selector_by == "ls" or selector_by == 'links':
                ele = wait_driver.until(
                    lambda x: x.find_elements_by_link_text(selector_value)[int(index)])
            elif selector_by == "ps" or selector_by == 'partial_link_texts':
                ele = wait_driver.until(
                    lambda x: x.find_elements_by_partial_link_text(selector_value)[int(index)])
            elif selector_by == "ts" or selector_by == 'tag_names':
                ele = wait_driver.until(lambda x: x.find_elements_by_tag_name(selector_value)[int(index)])
            elif selector_by == "xs" or selector_by == 'xpaths':
                ele = wait_driver.until(lambda x: x.find_elements_by_xpath(selector_value)[int(index)])
            elif selector_by == "as" or selector_by == 'android_uiautomators':
                ele = wait_driver.until(
                    lambda x: x.find_elements_by_android_uiautomator(selector_value)[int(index)])
            else:
                raise NameError("Please enter a valid type of targeting elements.")
        else:
            if selector_by == "i" or selector_by == 'id':
                ele = helper.get_appium().find_element_by_id(selector_value)
            elif selector_by == "n" or selector_by == 'name':
                ele = helper.get_appium().find_element_by_xpath("//*[@text='" + selector_value + "']")
            elif selector_by == "c" or selector_by == 'class_name':
                ele = helper.get_appium().find_element_by_class_name(selector_value)
            elif selector_by == "l" or selector_by == 'link':
                ele = helper.get_appium().find_element_by_link_text(selector_value)
            elif selector_by == "p" or selector_by == 'partial_link_text':
                ele = helper.get_appium().find_element_by_partial_link_text(selector_value)
            elif selector_by == "t" or selector_by == 'tag_name':
                ele = helper.get_appium().find_element_by_tag_name(selector_value)
            elif selector_by == "x" or selector_by == 'xpath':
                ele = helper.get_appium().find_element_by_xpath(selector_value)
            elif selector_by == "a" or selector_by == 'android_uiautomator':
                # selector_value = new UiSelector().resourceId(\"com.xingjiabi.shengsheng:id/cbReview\").checked(false)
                ele = helper.get_appium().find_element_by_android_uiautomator(selector_value)
            elif selector_by == "is" or selector_by == 'ids':
                ele = helper.get_appium().find_elements_by_id(selector_value)[int(index)]
            elif selector_by == "ns" or selector_by == 'names':
                ele = helper.get_appium().find_elements_by_xpath("//*[@text='" + selector_value + "']")[int(index)]
            elif selector_by == "cs" or selector_by == 'class_names':
                ele = helper.get_appium().find_elements_by_class_name(selector_value)[int(index)]
            elif selector_by == "ls" or selector_by == 'links':
                ele = helper.get_appium().find_elements_by_link_text(selector_value)[int(index)]
            elif selector_by == "ps" or selector_by == 'partial_link_texts':
                ele = helper.get_appium().find_elements_by_partial_link_text(selector_value)[int(index)]
            elif selector_by == "ts" or selector_by == 'tag_names':
                ele = helper.get_appium().find_elements_by_tag_name(selector_value)[int(index)]
            elif selector_by == "xs" or selector_by == 'xpaths':
                ele = helper.get_appium().find_elements_by_xpath(selector_value)[int(index)]
            elif selector_by == "ss" or selector_by == 'selector_selectors':
                ele = helper.get_appium().find_elements_by_css_selector(selector_value)[int(index)]
            elif selector_by == "as" or selector_by == 'android_uiautomators':
                # selector_value = new UiSelector().resourceId(\"com.xingjiabi.shengsheng:id/cbReview\").checked(false)
                ele = helper.get_appium().find_elements_by_android_uiautomator(selector_value)[int(index)]
            else:
                raise NameError("Please enter a valid type of targeting elements.")
    except Exception as e:
        oper.log(str(selector) + "找不到元素: " + str(e), 2)
        raise check.TouchException(str(selector) + "找不到元素: " + str(e))
    return ele


if __name__ == '__main__':
    element('x,//android.widget.TabWidget/android.widget.RelativeLayout[5]/android.widget.ImageView[1]')
