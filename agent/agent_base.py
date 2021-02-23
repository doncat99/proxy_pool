#! /usr/bin/env python
# -*- coding: utf-8 -*-

class Agent(object):
    proxies = []

    def extract_proxy(self):
        raise NotImplementedError

    def register(self):
        Agent.proxies.append(self)
        return self
