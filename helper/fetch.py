# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     fetchScheduler
   Description :
   Author :        JHao
   date：          2019/8/6
-------------------------------------------------
   Change Activity:
                   2019/08/06:
-------------------------------------------------
"""
__author__ = 'JHao'

from handler.logHandler import LogHandler
from handler.proxyHandler import ProxyHandler
from handler.configHandler import ConfigHandler
from agent.agent_base import Agent

class Fetcher(object):
    name = "fetcher"

    def __init__(self):
        self.log = LogHandler(self.name)
        self.conf = ConfigHandler()
        self.proxy_handler = ProxyHandler()

    def fetch(self):
        """
        fetch proxy into db with proxyFetcher
        :return:
        """
        proxy_set = set()
        self.log.info("ProxyFetch : start")
        for agent in Agent.proxies:
            fetcher = agent()
            fetch_name = fetcher.__class__.__name__
            try:
                for proxy in fetcher.extract_proxy():
                    if proxy in proxy_set:
                        self.log.info('ProxyFetch - %s: %s exist' % (fetch_name, proxy.ljust(23)))
                        continue
                    else:
                        self.log.info('ProxyFetch - %s: %s success' % (fetch_name, proxy.ljust(23)))
                    if proxy.strip():
                        proxy_set.add(proxy)
            except Exception as e:
                self.log.error("ProxyFetch - {func}: error".format(func=fetch_name))
                self.log.error(str(e))
        self.log.info("ProxyFetch - all complete!")
        return proxy_set


def runFetcher():
    return Fetcher().fetch()
