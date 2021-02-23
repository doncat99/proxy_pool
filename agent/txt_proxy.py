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
class TxtProxy(Agent):
    def __init__(self):
        self.re_ip_port_pattern = re.compile(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):([\d]{1,5})")

        self.txt_list = [
            # 'http://api.xicidaili.com/free2016.txt',
            'http://static.fatezero.org/tmp/proxy.txt',
            'http://pubproxy.com/api/proxy?limit=20&format=txt&type=http',
            'http://comp0.ru/downloads/proxylist.txt',
            'http://www.proxylists.net/http_highanon.txt',
            'http://www.proxylists.net/http.txt',
            'http://ab57.ru/downloads/proxylist.txt',
            'https://www.rmccurdy.com/scripts/proxy/good.txt'
        ]

    def extract_proxy(self):
        for url in self.txt_list:
            try:
                rp = WebRequest().get(url, timeout=10)

                re_ip_port_result = self.re_ip_port_pattern.findall(rp.text)

                if not re_ip_port_result:
                    raise Exception("empty")

                for host, port in re_ip_port_result:
                    yield f'{host}:{port}'

            except:
                pass


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
