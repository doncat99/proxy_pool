#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals, absolute_import, division, print_function

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
class JiangXianLiProxy(Agent):
    def __init__(self):
        self.url = 'http://ip.jiangxianli.com/?country=中国&page={}'

    def extract_proxy(self):
        """
        http://ip.jiangxianli.com/?page=
        免费代理库
        :return:
        """
        page_count = 1
        for i in range(1, page_count + 1):
            url = self.url.format(i)
            html_tree = WebRequest().get(url).tree
            for index, tr in enumerate(html_tree.xpath("//table//tr")):
                if index == 0:
                    continue
                yield ":".join(tr.xpath("./td/text()")[0:2]).strip()


if __name__ == '__main__':
    p = Agent.proxies[0]()
    for proxy in p.extract_proxy():
        print(proxy)
