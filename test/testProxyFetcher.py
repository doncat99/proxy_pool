# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     testProxyFetcher
   Description :
   Author :        JHao
   date：          2020/6/23
-------------------------------------------------
   Change Activity:
                   2020/6/23:
-------------------------------------------------
"""
__author__ = 'JHao'

from agent.agent_base import Agent


def testProxyFetcher():
    for agent in Agent.proxies:
        fetcher = agent()
        fetch_name = fetcher.__class__.__name__
        proxy_count = 0
        for proxy in fetcher.extract_proxy():
            if proxy:
                print('{func}: fetch proxy {proxy},proxy_count:{proxy_count}'.format(func=fetch_name, proxy=proxy,
                                                                                     proxy_count=proxy_count))
                proxy_count += 1


if __name__ == '__main__':
    testProxyFetcher()
