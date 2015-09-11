#!/usr/bin/env python
# coding: utf-8
import sys
import base64
from output import OutPut
import mysql_util as MU
reload(sys)
sys.setdefaultencoding('utf-8')

class MysqlMonitor:
    MysqlFailure = "MYSQL_FAILURE"

class WriteMysql(OutPut):

    def __init__(self, cfg):
        self.sql = "insert into app_feature(%s) values(%s) on duplicate key update %s;"
        self.host = cfg.get("mysql", "host")
        self.port = cfg.getint("mysql", "port")
        self.user = cfg.get("mysql", "user")
        self.passwd = cfg.get("mysql", "passwd")
        self.db = cfg.get("mysql", "db")
        self.pool_size = cfg.getint("mysql", "pool_size")
        MU.registerConnection("app_feature", self.host, self.port, self.user, 
                          self.passwd, self.db, self.pool_size)

    def output(self, out_dict):
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
            
#print sql
            ret = MU.fetchall("app_feature", sql)
            #if not ret:
            #    self.monitor(MysqlMonitor.MysqlFailure)

            return True, "SUCC"
        except Exception, why:
            self.logger.warn("fail to write to mysql[%s][%s]" %(out_dict, why))
            return None, "exception[%s]" %(why)


if __name__ == '__main__':

    wm = WriteMysql()
    
    out_dict = {'latest_release_time': u'"2012-05-18T01:28:40Z"', 'pkg_size': u'16667866', 'score':
                4.0, 'pkg_name': u'"com.oreilly.fluent"', 'pkg_category': u'"Reference"', 'appid':'526533240', 'usercount': 5}
    stat, stat_str = wm.output(out_dict)
    print stat_str
