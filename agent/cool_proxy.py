#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

import re
import time
import codecs
import base64
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
class CoolProxy(Agent):
    def __init__(self):
        self.url = 'http://www.cool-proxy.net/proxies/http_proxy_list/sort:score/direction:desc/page:{page}'
        self.re_ip_encode_pattern = re.compile(r'Base64.decode\(str_rot13\("([^"]+)"\)\)', re.I)
        self.re_port_pattern = re.compile(r'<td>(\d{1,5})</td>', re.I)

    def extract_proxy(self, pages=10):
        for page_num in range(1, pages):
            try:
                rp = WebRequest().get(self.url.format(page=page_num), timeout=10)

                re_ip_encode_result = self.re_ip_encode_pattern.findall(rp.text)
                re_port_result = self.re_port_pattern.findall(rp.text)

                if not len(re_ip_encode_result) or not len(re_port_result):
                    raise Exception("empty")

                if len(re_ip_encode_result) != len(re_port_result):
                    raise Exception("len(host) != len(port)")

                for index, each_result in enumerate(re_ip_encode_result):
                    decode_ip = base64.b64decode(codecs.decode(each_result.strip(), 'rot-13')).strip()
                    host = decode_ip.decode('utf-8')
                    port = re_port_result[index]
                    yield f'{host}:{port}'

            except:
                continue

            time.sleep(3)


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
