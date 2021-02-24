#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import time
import logging

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from agent import Agent
from util.webRequest import WebRequest

logger = logging.getLogger(__name__)


@Agent.register
class KuaiProxy(Agent):
    def __init__(self):
        self.urls = [
            'https://www.kuaidaili.com/free/inha/{}/',
            'https://www.kuaidaili.com/free/intr/{}/'
        ]

    def extract_proxy(self):
        """
        快代理 https://www.kuaidaili.com
        """
        for url in self.urls:
            page_count = 1
            url_list = []
            for page_index in range(1, page_count + 1):
                url_list.append(url.format(page_index))

            for url in url_list:
                tree = WebRequest().get(url).tree
                proxy_list = tree.xpath('.//table//tr')

                # 必须sleep 不然第二条请求不到数据
                time.sleep(1)

                for tr in proxy_list[1:]:
                    yield ':'.join(tr.xpath('./td/text()')[0:2])


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
