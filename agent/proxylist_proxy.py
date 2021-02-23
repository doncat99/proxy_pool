#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import re
import time
import base64
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
class ProxyListProxy(Agent):
    def __init__(self):
        self.url = 'http://proxy-list.org/english/index.php?p={page}'  # 从1-10
        self.re_ip_port_encode_pattern = re.compile(r"Proxy\(\'([\w\d=+]+)\'\)", re.I)

    def extract_proxy(self, pages=10):
        for page_num in range(1, pages):
            try:
                rp = WebRequest().get(self.url.format(page=page_num), timeout=10)
                re_ip_port_encode_result = self.re_ip_port_encode_pattern.findall(rp.text)

                if not re_ip_port_encode_result:
                    raise Exception("empty")

                for each_result in re_ip_port_encode_result:
                    decode_ip_port = base64.b64decode(each_result).decode('utf-8')
                    host, port = decode_ip_port.split(':')
                    yield f'{host}:{port}'

            except:
                continue

            time.sleep(3)


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
