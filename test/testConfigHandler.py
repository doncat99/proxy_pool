# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     testGetConfig
   Description :   testGetConfig
   Author :        J_hao
   date：          2017/7/31
-------------------------------------------------
   Change Activity:
                   2017/7/31:
-------------------------------------------------
"""
__author__ = 'J_hao'

from handler.configHandler import ConfigHandler
from time import sleep


def testConfig():
    """
    :return:
    """
    conf = ConfigHandler()
    print(conf.dbConn)
    print(conf.serverPort)
    print(conf.serverHost)
    print(conf.tableName)


if __name__ == '__main__':
    testConfig()

