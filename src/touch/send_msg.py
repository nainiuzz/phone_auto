#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# http://www.runoob.com/python/python-email.html
# http://help.163.com/09/1224/17/5RAJ4LMH00753VB8.html
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr

import oper
import helper


def send_mail(sender=helper.read_config_item("send_msg", "sender"),
              password=helper.read_config_item("send_msg", "password"),
              receivers=helper.read_config_item("send_msg", "receivers"),
              result=None):
    if result:
        content = """
                <p style="color:#000;font-family:'微软雅黑',Helvetica,Arial,sans-serif;">尊敬的开发者：</p> 
                <p style="color:#000;font-family:'微软雅黑',Helvetica,Arial,sans-serif;">UI自动化测试执行结果：</p> 
                <p style="color:#000;font-family:'微软雅黑',Helvetica,Arial,sans-serif;">%s</p>
                <p><a href="http://j9.test.k8s.taqu.cn/tq-qtp/index" style="color: red;
                font-family:'微软雅黑',Helvetica,Arial,sans-serif;">请前往平台查看结果！</a></p>
                """ % (str(result))
    else:
        content = """
                <p style="color:#000;font-family:'微软雅黑',Helvetica,Arial,sans-serif;">尊敬的开发者：</p> 
                <p style="color:#000;font-family:'微软雅黑',Helvetica,Arial,sans-serif;">UI自动化测试执行结果：</p>
                <p><a href="http://j9.test.k8s.taqu.cn/tq-qtp/index" style="color: red; 
                font-family:'微软雅黑',Helvetica,Arial,sans-serif;">请前往平台查看结果！</a></p>
                """
    subject = "UI自动化测试"
    message = MIMEText(content, 'html', 'utf-8')
    message['Subject'] = Header(subject, "utf-8").encode()
    message['From'] = _format_addr('UI自动化测试系统 <%s>' % sender)
    message['To'] = ';'.join(receivers)
    obj = smtplib.SMTP(helper.read_config_item("email", "host"), helper.read_config_item("email", "port"))
    obj.login(sender, password)
    try:
        obj.sendmail(sender, receivers, message.as_string())
        oper.log("邮件发送成功")
    except smtplib.SMTPException as e:
        oper.log("邮件无法发送！" + str(e), 2)
    except Exception as e:
        oper.log(e, 2)
    finally:
        obj.quit()


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


if __name__ == "__main__":
    # sender_mail = 'naopyani@163.com'
    # passwords = "wzh20353634689"
    # receiver_dict = ["lushan@taqu.cn"]
    results = {'id': '1030', 'case_info': [
        '{"file_path": "caseUI/Me/SetUp/AboutTouch.xml", '
        '"test_result_info": "执行测试前置用例【caseUI/Me/Login/Logout.xml】的第step8个用例步骤失败，'
        '原因是：id,com.xingjiabi.shengsheng:id/login_off_layout该对象不存在;成功;成功;成功;'
        '执行测试用例【case1】的第step4个用例步骤失败，原因是：关于我们该文字不存在;成功", "status": "0"}']}
    send_mail(result=results)
