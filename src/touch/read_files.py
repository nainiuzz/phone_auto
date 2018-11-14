#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# https://blog.csdn.net/huagangwang/article/details/78274177
import os
import shutil
import oper
import helper


# 打开共享文件夹，从服务器下载文件
def share_download():
    """
    打开共享文件夹，从服务器下载apk文件
    """
    path = helper.read_config_item("apk", "path")
    try:
        oper.log("开始下载共享文件夹，读取文件...")
        get_file_dir_download(path)
    except Exception as e:
        oper.log("打开共享文件夹，从服务器下载文件失败：" + str(e), 2)


def get_file_dir_download(share_path):
    """
    下载文件
    :param share_path: 共享文件夹路径
    """
    try:
        file_list = os.listdir(share_path)
        for file in file_list:
            file_path = os.path.join(share_path, file)
            if os.path.isfile(file_path):
                # 如果是文件，就复制
                copy_file_down(file_path)
    except Exception as e:
        oper.log("下载到本地失败：" + str(e), 2)


def copy_file_down(paths, local_path=None):
    """
    # 复制文件或文件夹到本地
    :param paths:拷贝路径
    :param local_path:到本地路径
    :return:
    """
    if local_path:
        local_path = local_path
    else:
        local_path = helper.srcPath + '/common/'
    try:
        new_path = shutil.copy(paths, local_path)
        oper.log(str(new_path) + "复制成功！")
    except Exception as e:
        oper.log("复制到本地失败：" + str(e), 2)


def exist_apk(apk_name):
    """
    判断本地是否存在apk，如果不存在下载
    :param apk_name: apk名称
    :return: 更新apk
    """
    dirs = str(apk_name).split("/")[0].split(":")[1]
    apk = str(apk_name).split("/")[1]
    local_path = helper.srcPath + '/common/' + dirs
    share_path = helper.read_config_item("apk", "path")
    if not os.path.exists(local_path):
        # 创建目录
        os.makedirs(local_path)
        oper.log("创建apk目录：" + str(local_path))
    file_list = os.listdir(local_path)
    if apk not in file_list:
        file_path = os.path.join(share_path, apk)
        copy_file_down(file_path, local_path)


def del_apk(apk_name):
    """
    判断本地是否存在apk，如果存在就删除
    :param apk_name: apk名称
    :return:
    """
    dirs = str(apk_name).split("/")[0].split(":")[1]
    apk = str(apk_name).split("/")[1]
    local_path = helper.srcPath + '/common/' + dirs + '/' + apk
    if os.path.exists(local_path):
        try:
            os.remove(local_path)
            oper.log(str(local_path) + "本地apk,删除成功")
        except Exception as e:
            oper.log(str(local_path) + "本地apk,删除失败" + str(e), 2)


if __name__ == "__main__":
    # share_download()
    exist_apk("127.0.0.1:62026/app-auto-release-7044.apk")
    del_apk("127.0.0.1:62026/app-auto-release-7044.apk")
