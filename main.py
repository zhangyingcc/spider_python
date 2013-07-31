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

LOG_ADDRESS = '/usr/local/var/log/spider_logging.txt'                   #日志文件地址
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'     #日志格式
LOG_LEVEL = logging.DEBUG                                               #日志级别
REDIS_IP = '127.0.0.1'                                                  #Redis的ip
REDIS_PORT = 6379                                                       #Redis的port
REDIS_FREQUENCE = 10                                                    #Redis清空的频率
SPIDER_KEYS = (u'校招', u'应届', u'毕业生')                             #筛选的关键词

def init_log():
    logger = logging.getLogger() 
    handler = logging.FileHandler(LOG_ADDRESS)
    formatter = logging.Formatter(LOG_FORMAT) 
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
    return logger

def init_params():
    return (
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
        #去除置顶贴
        if line.parent.parent.get('class') == 'top':
            continue
        line['href'] = host + line['href']
        title = line.string
        if filter(lambda x: x in title, SPIDER_KEYS):
            rs.sadd('urls', line)

def main():
    logger = init_log()
    logger.info('spider start!')

    rs = redis.Redis(host=REDIS_IP, port=REDIS_PORT)
    rs.incr('times')
    if int(rs.get('times')) >= REDIS_FREQUENCE:
        rs.flushall()

    params = init_params()

    for param in params :
        spider(rs, param['host'], param['url'], param['headers'], param['href'])

    logger.info("spider finish!\n") 

if __name__ == '__main__':
    main()
