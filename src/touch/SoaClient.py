#!/usr/bin/env python
# encoding:utf-8

from urllib.parse import urlencode
import urllib.request
import json
import base64
import uuid
import helper
import oper

ENV = helper.read_config_item("soa_config", "env")
SOA_CLIENT = helper.read_config_item("soa_config", "soa_client")
SOA_SYSTEM = helper.read_config_item("soa_config", "soa_system")


class SoaClient(object):
    _host_name = ""
    _host = ""
    _service = ""
    _method = ""

    @staticmethod
    def get_soa(host_name, service):
        # soa_client = json.loads(str(SOA_CLIENT), encoding='utf-8')
        host = SOA_CLIENT.get(host_name)

        return SoaClient(host_name, host, service)

    def __init__(self, host_name, host, service):
        self._host_name = host_name
        self._host = host
        self._service = service

    def __getattr__(self, method):
        self._method = method

        def func(*param):
            return self.get_result(param)

        return func

    def get_result(self, *form):
        """
        模拟 soa 请求
        :return: obj
        """
        if self._service is None or self._method is None:
            return {}

        if SOA_SYSTEM.get(self._host_name, "php") == 'php':
            url = "%s/jService?distinctRequestId=%s&env=%s&service=%s&method=%s" % (
                self._host, str(uuid.uuid1()).replace('-', ''), str(ENV), self._service, self._method)
        else:
            url = "%s?distinctRequestId=%s&env=%s&service=%s&method=%s" % (
                self._host, str(uuid.uuid1()).replace('-', ''), str(ENV), self._service, self._method)
        data_str = json.dumps(form[0])
        data_bytes = data_str.encode('utf-8')
        data = urlencode({"form": base64.b64encode(data_bytes)}).encode(encoding='utf-8')

        try:
            request = urllib.request.Request(url, data)
            response = urllib.request.urlopen(request)
            results = response.read()
            if results is not None:
                try:
                    rs = json.loads(results)
                    # 和0的判断是java的，php不一样
                    if rs.get("code") and rs.get("code") != '0':
                        return "", u"异常信息：%s:%s" % (rs['code'], rs['msg'])
                    else:
                        return rs.get("data"), ""

                except Exception as e:
                    return "", str(e)

            return True, results
        except Exception as e:
            return "", str(e)

        # return "", "unknown"


# 获取MQ队列信息, 'operation' 服务名，autoTest。uiTestCallback()方法名
def get_mq():
    soa = SoaClient.get_soa('tqmq', 'operation')
    # res, error = soa.pop(0)
    resp, error = soa.pop('queue_case_ui_test', 3600)
    if error:
        oper.log(u"获取队列失败，异常：" + error)
    if resp:
        if resp['msg_id']:
            oper.log(u"哇！队列终于来消息啦！开始吧。")
    return resp


# 删除队列消息Celery python
def del_mq(resp):
    soa = SoaClient.get_soa('tqmq', 'operation')
    _, error = soa.remove('queue_case_ui_test', resp['msg_id'])
    if error:
        oper.log("删除队列发送异常：%s" % error, 2)
        pass
    if not _:
        oper.log("删除队列失败，返回信息为None", 2)


# 返回队列信息, 结果json数据
def back_mq(result_json):
    soa_ui = SoaClient.get_soa('ui_auto', 'autoTest')
    resp, error = soa_ui.uiTestCallback(result_json["id"], result_json["case_info"])
    if error:
        oper.log("回调队列失败，异常：" + error, 2)


# 请求账号池
def get_pool():
    soa_ui = SoaClient.get_soa('ui_auto', 'caseUIAccountPool')
    try:
        resp, error = soa_ui.getList()
        if error:
            oper.log("请求账号池失败，异常：" + error, 2)
        if not resp:
            return {}
        else:
            return resp
    except Exception as e:
        oper.log("请求账号池失败，异常：" + str(e), 2)
        return {}


if __name__ == '__main__':
    get_pool()
    print(1)
    # res = get_mq()
    # del_mq(res)
    # result = {'id': '5304', 'case_info': [
    #     "{'file_path': 'caseUI/test/11.xml', 'test_result_info': URLError(ConnectionRefusedError(10061, "
    #     "'由于目标计算机积极拒绝，无法连接。', None, 10061, None),), 'status': '0'}"]}
    # back_mq(result)
