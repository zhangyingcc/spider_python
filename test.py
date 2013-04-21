#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import requests

def main():
    #url = 'http://bbs.byr.cn/board/Job'
    url = 'http://bbs.byr.cn/article/JobInfo/89292'
    headers = {
        "X-Requested-With" : "XMLHttpRequest",  
    }
    payload = {
        #'p': '1',
    }
    r = requests.get(url, headers = headers, params = payload)
    text = r.text
    print text

if __name__ == '__main__':
    main()
