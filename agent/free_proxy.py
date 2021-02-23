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
class FreeProxy(Agent):
    def __init__(self):
        self.url = 'https://free-proxy-list.net/'
        self.re_ip_port_pattern = re.compile(
            r"<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td><td>(\d{1,5})</td>", re.I)

    def extract_proxy(self, page_num=0):
        try:
            rp = WebRequest().get(self.url.format(page=page_num), timeout=10)
            re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)
            for host, port in re_ip_port_result:
                yield f'{host}:{port}'

        except:
            pass


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
