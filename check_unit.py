#!/usr/bin/env python
# -*- coding: utf-8 -*-
__version__ = '1.0.0.2'

"""
@brief 简介 
@details 详细信息
@author  wuxiaosheng
@date    2016-03-31 
"""
import sys
import re
import json
import codecs
import time
import pymongo


class CheckCmdb(object):
    def __init__(self, host='localhost', port=27017):
        self.conn = pymongo.MongoClient(host, port)
        self.db = self.conn.dcs_cmdb
        self.relations = self.db.relations
        self.resources = self.db.resources

    def scan_cmdb(self):
        """
        浏览cmdb数据库
        :return:
        """
        res = self.resources.find()
        for item in res:
            try:
                
                if int(item['attributes']['ci_type']) == 3:
                    print item['resource_id'], item['attributes']['name'], item['attributes'].get('unit')
                    item['attributes']['unit'] = 'C'
                    self.update(item)
                
                if int(item['attributes']['ci_type']) == 2 and not item['resource_id'].startswith('0_'):
                    print item['resource_id'], item['attributes']['name']
                    item['attributes']['ci_type'] = '20'
                    self.update(item)
            except Exception as e:
                pass

    def update(self, item):
        """
        通用更新操作
        :param item:
        :return:
        """
        self.resources.update({'_id': item['_id']}, {'$set': {'attributes': item['attributes']}})


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print sys.argv
    cmdb = CheckCmdb('localhost', 27017)
    cmdb.scan_cmdb()
