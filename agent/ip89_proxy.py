#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import re
import logging

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from agent.agent_base import Agent
from util.webRequest import WebRequest

logger = logging.getLogger(__name__)


@Agent.register
class Ip89Proxy(Agent):
    def __init__(self):
        self.url = 'http://www.89ip.cn/index_{}.html'

    def extract_proxy(self):
        """
        http://www.89ip.cn/index.html
        89免费代理
        :param max_page:
        :return:
        """
        max_page = 2
        for page in range(1, max_page + 1):
            url = self.url.format(page)
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(
                r'<td.*?>[\s\S]*?(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})[\s\S]*?</td>[\s\S]*?<td.*?>[\s\S]*?(\d+)[\s\S]*?</td>',
                r.text)
            for proxy in proxies:
                yield ':'.join(proxy)


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
