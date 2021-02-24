#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import re
import logging
import time

import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from util.webRequest import WebRequest
from agent import Agent

logger = logging.getLogger(__name__)


@Agent.register
class CnProxy(Agent):
    def __init__(self):
        self.url = 'http://www.cnproxy.com/proxy{page}.html'  # 从1-10
        self.re_ip_pattern = re.compile(r'<tr><td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<SCRIPT', re.I)
        self.re_port_encode_pattern = re.compile(r'javascript>document.write\(":"([+\w]{2,10})\)</SCRIPT>')

        self.port_dict = {
            'v': '3',
            'm': '4',
            'a': '2',
            'l': '9',
            'q': '0',
            'b': '5',
            'i': '7',
            'w': '6',
            'r': '8',
            'c': '1',
            '+': ''
        }

    def extract_proxy(self, pages=10):
        for page_num in range(1, pages):
            try:
                rp = WebRequest().get(self.url.format(page=page_num), timeout=10)

                re_ip_result = self.re_ip_pattern.findall(rp.text)
                re_port_encode_result = self.re_port_encode_pattern.findall(rp.text)

                if not len(re_ip_result) or not len(re_port_encode_result):
                    raise Exception("empty")

                if len(re_ip_result) != len(re_port_encode_result):
                    raise Exception("len(host) != len(port)")

                for index, each_result in enumerate(re_port_encode_result):
                    each_result = each_result.strip()
                    host = re_ip_result[index]
                    port = int(''.join(list(map(lambda x: self.port_dict.get(x, ''), each_result))))
                    yield f'{host}:{port}'

            except:
                continue

            time.sleep(3)


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
