# -*- coding: utf-8 -*-
import os
import time
import json
import requests

import geoip2.database

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
geoip_reader = geoip2.database.Reader(os.path.join(base_dir, 'data/GeoLite2-Country.mmdb'))

rp = requests.get('http://httpbin.org/get')
origin_ip = rp.json().get('origin', '')


def _check_proxy_anonymity(response_json):
    via = response_json.get('headers', {}).get('Via', '')

    if origin_ip in json.dumps(response_json):
        return 'transparent'
    elif via and via != "1.1 vegur":
        return 'anonymous'
    else:
        return 'high_anonymous'


def _updateProxyInfo(proxy_object, scheme):
    request_proxies = {scheme: proxy_object.proxy}
    request_begin = time.time()

    try:
        response_json = requests.get(
                "%s://httpbin.org/get?show_env=1&cur=%s" % (scheme, request_begin),
                proxies=request_proxies,
                timeout=5).json()
    except:
        return None

    request_end = time.time()

    if str(request_begin) != response_json.get('args', {}).get('cur', ''):
        return None

    # set response time
    proxy_object.response_time = round(request_end - request_begin, 2)

    # set anonymity
    proxy_object.anonymity = _check_proxy_anonymity(response_json)

    # set country
    try:
        host = proxy_object.proxy.split(':')[0]
        proxy_object.country = proxy_object.country or geoip_reader.country(host).country.iso_code
    except:
        pass

    # set scheme
    proxy_object.scheme = scheme

    return proxy_object


def updateProxyInfo(proxy_object):
    for scheme in ["https", "http"]:
        result = _updateProxyInfo(proxy_object, scheme)
        if result is not None:
            return result
    return proxy_object
