# UI自动化测试框架
## 解释说明
    基于appium和python语言封装的自动化测试库
### touch项目框架结构
    ui_auto_test--项目名称
    ui_auto_test/resource--json文件，储存数据进行调用
    ui_auto_test/src--存储核心内容
    ui_auto_test/src/common--存放驱动的，可根据浏览器版本更改驱动
    ui_auto_test/src/config--配置文件，存储环境数据
    ui_auto_test/src/touch--存放各个模块核心方法
    ui_auto_test/src/log--存放日志信息
    ui_auto_test/src/check--检查动作
    ui_auto_test/src/find--查找动作
    ui_auto_test/src/helper--环境切换和一些辅助方法
    ui_auto_test/src/oper--操作
    ui_auto_test/src/oper_action--针对xml文件解析触发动作
    ui_auto_test/test--测试用例模块
    ui_auto_test/test/test_model--调试核心方法文件
    ui_auto_test/conftest--配置测试报告
    ui_auto_test/report--测试报告
    ui_auto_test/testSuite--扫描获取test__开头的py文件
### 目前支持的操作动作
```
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
            'continuous_click': oper.continuous_click,
            'get_text': oper.get_text,
            'get_attr': oper.get_attr,
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
            'action_move_to': oper.action_move_to,
            'action_move_to_xy': oper.action_move_to,
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
            "cal_notequal": oper.CalStyle().notequal
        }
```
### [模拟器安装说明](https://www.jianshu.com/p/50eb9a88f4e2)

    1、下载[夜神模拟器](https://www.yeshen.com/)

    2、配置系统环境：在Path中添加D:\yeShen\Nox\bin

    3、cmd 输入nox_adb.exe connect 127.0.0.1:62025

    4、如果出现问题：将SDK目录下的adb.exe文件，复制到夜神模拟器的目录下，因为夜神模拟器目录下原本的adb文件名字叫做nox_adb.exe，因此复制过去之后也得改名为nox_adb.exe

    5、在D:\yeShen\Nox\bin nox_adb.exe connect 127.0.0.1:62001

    6、输入adb devices，验证是否连接成功

### appium的并发测试

    Appium提供了在一台设备上启动多个Android会话的方案，而这个方案需要你输入不同的指令来启动多个Appium服务来实现。

    启动多个Android会话的重要指令包括：

    -p Appium的主要端口

    -U 设备id

    -bp Appium bootstrap端口

    --chromedriver-port chromedriver端口（当使用了webviews或者chrome）

    --selendroid-port selendroid端口（当使用了selendroid）

### [回调接口文档](http://10.10.50.205:1234/java/qtp_system/uiTestCallback)
