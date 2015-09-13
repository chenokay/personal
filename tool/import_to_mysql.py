#!/usr/bin/env python
# coding: utf-8

import to_mysql
import os
import sys
import time
import datetime
reload(sys)
sys.setdefaultencoding('utf-8')

class ImportMysql:
    def __init__(self):
        self.tag_dict = {}

    def load_tag(self, path):
        fd = open(path)
        for tl in fd:
            line = tl.strip()
            items = line.split('\t')
            if len(items) < 2:
                print 'tag line format error:%s' %(tl)
                continue
            self.tag_dict[items[0]] = items[1]

    def run(self, path):
        mhandle = to_mysql.WriteMysql('product')
        self.load_tag(path)

        line = sys.stdin.readline()

        while line:
            items = line.split('####')
            if len(items) != 6:
                print 'product line format error:%s' %(line)
                continue
            ts=int(time.time())
            d = datetime.datetime.fromtimestamp(ts)
            timestamp = d.strftime("%Y%m%d")
            field_dict = {}
            field_dict['dt'] = timestamp
            field_dict['product_name'] = '\'' + items[1] + '\''
            field_dict['product_link'] = '\'' +items[0]+ '\''
            field_dict['product_img'] = '\'' +items[4]+ '\''
            field_dict['static_weight'] = items[5].strip()
            if items[2] in self.tag_dict:
                field_dict['category'] = self.tag_dict[items[2]]
            else:
                field_dict['category'] = 0

            sql_vec = []
            main_sql = mhandle.compose(field_dict)
            sql_vec.append(main_sql)

            sub_category = items[3]

            cat_vec = sub_category.split('*')

            for sc in cat_vec:
                if sc in self.tag_dict:
                    sub_sql = 'insert into product_sub_category(product_id, sub_category) values(LAST_INSERT_ID(), %s)' %(self.tag_dict[sc])
                    sql_vec.append(sub_sql)
                else:
                    print 'NULL_sub_category :%s does not exist' %(sc)

            print ';'.join(sql_vec)

            line = sys.stdin.readline()



if __name__ == '__main__':
    import_mysql = ImportMysql()
    import_mysql.run('/root/personal/mysql/category_tag')
