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
import oper_action
import SoaClient
import time
import oper
import json


def test_run():
    while True:
        res = SoaClient.get_mq()
        if res and res["msg_body"]:
            result_detail = {"id": "", "case_info": []}
            result_detail = json.dumps(result_detail, ensure_ascii=False)
            result_json = json.loads(result_detail, encoding="utf-8")
            case_info = oper_action.TaskAction(res).read_case_info()
            task_info = oper_action.TaskAction(res).read_base_info()
            task_id = task_info["id"]
            result_json["id"] = task_id
            result_case = []
            flag = 0
            init_detail = ""
            try:
                oper_action.TaskAction(res).initial_appium()
            except Exception as e:
                oper.log("appium启动app失败：" + str(e), 2)
                init_detail = "appium启动app失败：" + str(e)
                flag = 1
            for case_id in case_info:
                result_info = oper_action.SaveResult()
                save_param = oper_action.SaveValue()
                case_message = {}
                case_message["file_path"] = case_id
                if flag == 1:
                    case_message["test_result_info"] = init_detail
                    case_message["status"] = "0"
                else:
                    try:
                        message = "%s | %s | %s | %s | " % (
                            task_info["app"], task_info["id"], task_info["current_version"],
                            case_id)
                        oper.log('执行测试用例【' + str(case_id) + '】', formats=message)
                        run = oper_action.RunXml(case_id, result_info.write_result, result_info.write_status,
                                                 save_param, message)
                        run.run()
                    except Exception as e:
                        oper.log(e, 2)
                        result_info.write_result(str(e))
                    case_message["test_result_info"] = result_info.get_result()
                    case_message["status"] = result_info.get_status()
                case_message = json.dumps(case_message, ensure_ascii=False)
                result_case.append(case_message)
            try:
                helper.release_appium()
            except Exception as e:
                oper.log("appium关闭app失败：" + str(e), 2)
            result_json["case_info"] = result_case
            result_json = json.dumps(result_json, ensure_ascii=False)
            response_json = json.loads(result_json, encoding="utf-8")
            oper.log(response_json)
            try:
                SoaClient.back_mq(response_json)
            except Exception as e:
                oper.log("返回队列信息失败：" + str(e), 2)
            try:
                SoaClient.del_mq(res)
            except Exception as e:
                oper.log("删除队列信息失败：" + str(e), 2)
        else:
            time.sleep(1)


if __name__ == '__main__':
    pytest.main(helper.get_pytest_param(sys.argv[0], ' --junitxml='))
