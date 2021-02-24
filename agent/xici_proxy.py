#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import time
import logging
import re

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from agent import Agent
from util.webRequest import WebRequest

logger = logging.getLogger(__name__)


@Agent.register
class XiCiProxy(Agent):
    def __init__(self):
        self.urls = [
            "http://www.xiladaili.com/putong/",
            "http://www.xiladaili.com/gaoni/",
            "http://www.xiladaili.com/http/",
            "http://www.xiladaili.com/https/"]

    def extract_proxy(self):
        for url in self.urls:
            r = WebRequest().get(url, timeout=10)
            ips = re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}", r.text)
            for ip in ips:
                yield ip.strip()


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
