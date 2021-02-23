#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import logging
import re

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from agent.agent_base import Agent
from util.webRequest import WebRequest

logger = logging.getLogger(__name__)


@Agent.register
class Ip3366Proxy(Agent):
    def __init__(self):
        self.urls = ['http://www.ip3366.net/free/?stype=1',
                     'http://www.ip3366.net/free/?stype=2'
                     ]

    def extract_proxy(self):
        """
        云代理 http://www.ip3366.net/free/
        :return:
        """
        for url in self.urls:
            r = WebRequest().get(url, timeout=10)
            proxies = re.findall(r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', r.text)
            for proxy in proxies:
                yield ":".join(proxy)


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
