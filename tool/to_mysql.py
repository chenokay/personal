#!/usr/bin/env python
# coding: utf-8
import sys
import base64
import mysql_util as MU
reload(sys)
sys.setdefaultencoding('utf-8')

class MysqlMonitor:
    MysqlFailure = "MYSQL_FAILURE"

class WriteMysql():

    def __init__(self, table):
        self.sql = "insert into product(%s) values(%s) on duplicate key update %s"
        self.host =  "127.0.0.1"
        self.port =  3306
        self.user = "root"
        self.passwd = "bin729830"
        self.db =  "business_sale"
        self.pool_size = 8
        self.table = table
        MU.registerConnection(self.table, self.host, self.port, self.user, 
                          self.passwd, self.db, self.pool_size)

    def compose(self, out_dict):
        try:
            meta_keys = ""
            values = ""
            k2v = ""
            for key in out_dict:
                if meta_keys != "":
                    meta_keys = meta_keys + ","
                    values = values + ","
                meta_keys = meta_keys + key
                values = values + str(out_dict[key])
                if key == "appid":
                    continue
                
                if k2v != "":
                    k2v = k2v + ","
                up_str = "%s=%s" %(key, str(out_dict[key]))
                k2v = k2v + up_str

            sql = self.sql %(meta_keys, values, k2v)
            
            return sql
            #ret = MU.fetchall(self.table, sql)
            #if not ret:
            #    self.monitor(MysqlMonitor.MysqlFailure)

            #return True, ret
        except Exception, why:
            print "exception[%s]" %(why)
            return None

if __name__ == '__main__':

    wm = WriteMysql()
    
    out_dict = {'latest_release_time': u'"2012-05-18T01:28:40Z"', 'pkg_size': u'16667866', 'score':
                4.0, 'pkg_name': u'"com.oreilly.fluent"', 'pkg_category': u'"Reference"', 'appid':'526533240', 'usercount': 5}
    stat, stat_str = wm.output(out_dict)
    print stat_str
