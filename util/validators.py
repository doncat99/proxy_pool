# -*- coding: utf-8 -*-

import requests
from re import findall
from handler.configHandler import ConfigHandler

conf = ConfigHandler()
validators = []


def validator(func):
    validators.append(func)
    return func


@validator
def formatValidator(proxy_obj):
    """
    检查代理格式
    :param proxy:
    :return:
    """
    verify_regex = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}"
    _proxy = findall(verify_regex, proxy_obj.proxy)
    return True if len(_proxy) == 1 and _proxy[0] == proxy_obj.proxy else False


@validator
def timeOutValidator(proxy_obj):
    """
    检测超时
    :param proxy:
    :return:
    """
    verifyUrl = conf.verifyHttpsUrl if proxy_obj.scheme == 'https' else conf.verifyHttpUrl

    proxies = {"http": "http://{proxy}".format(proxy=proxy_obj.proxy), "https": "https://{proxy}".format(proxy=proxy_obj.proxy)}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
               'Accept': '*/*',
               'Connection': 'keep-alive',
               'Accept-Language': 'zh-CN,zh;q=0.8'}
    try:
        r = requests.head(verifyUrl, headers=headers, proxies=proxies, timeout=conf.verifyTimeout, verify=False)
        if r.status_code == 200:
            return True
    except:
        pass
    return False


@validator
def customValidator(proxy_obj):
    """
    自定义validator函数，校验代理是否可用
    :param proxy:
    :return:
    """

    return True
