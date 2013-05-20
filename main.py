#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
#=============================================================================
#     FileName: main.py
#         Desc: 
#       Author: lizherui
#        Email: lzrak47m4a1@gmail.com
#     HomePage: https://github.com/lizherui
#      Version: 0.0.1
#   LastChange: 2013-04-21 17:12:36
#      History:
#=============================================================================
'''

import re
import requests
import redis
import logging
from BeautifulSoup import BeautifulSoup

def spider(rs, host, url, headers, href):
    r = requests.get(url, headers = headers)
    frs_soup = BeautifulSoup(r.text)
    frs_attrs = {
        'href' : re.compile(href),
        'title' : None,
        'target' : None,
    }
    frs_res =  frs_soup.findAll('a', frs_attrs)
    for line in frs_res:
        if line.parent.parent.get('class') == 'top':
            continue
        line['href'] = host + line['href']
        title = line.string
        keys = (u'校招', u'应届', u'毕业生')
        if filter(lambda x: x in title, keys):
            rs.sadd('urls', line)

def main():
    logger=logging.getLogger() 
    handler=logging.FileHandler("/usr/local/var/log/spider_logging.txt")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s') 
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    logger.info('start!')

    rs_host = 'localhost'
    rs_port = 6379
    rs = redis.Redis(host=rs_host, port=rs_port)
    rs.flushall()
    params = (
        {
            'host' : 'http://bbs.byr.cn',
            'url'  : 'http://bbs.byr.cn/board/JobInfo',
            'headers' : {
                "X-Requested-With" : "XMLHttpRequest",
            },
            'href' : "^/article/JobInfo/\d+$",
        },

        {
            'host' : 'http://www.newsmth.net',
            'url'  : 'http://www.newsmth.net/nForum/board/Career_Campus',
            'headers' : {
                "X-Requested-With" : "XMLHttpRequest",
            },
            'href' : "^/nForum/article/Career_Campus/\d+$",
        },
    )

    for param in params :
        spider(rs, param['host'], param['url'], param['headers'], param['href'])
    logger.info("end!\n") 

if __name__ == '__main__':
    main()
