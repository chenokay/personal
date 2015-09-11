#!/usr/bin/env python
# coding: utf-8

import web

class DataReader:
    def __init__(self):
        self.db = web.database(dbn='mysql', user='root', pw='bin729830', db='personal_page', host='127.0.0.1', port=3306)
        self.main_category_sql = 'SELECT product_name,product_img, product_link,static_weight FROM product where category=%s'
        self.sub_category_only_sql = 'SELECT  product_name,product_img, product_link,static_weight FROM product  JOIN product_sub_category ON product.id=product_sub_category.product_id and category=%s and product_sub_category.sub_category=%s'
        self.style_only_sql = 'SELECT product_name,product_img, product_link,static_weight FROM product LEFT JOIN product_style ON product.id=product_style.product_id and  category=%s  and product_style.style=%s'
        self.sub_category_and_style_sql = 'SELECT product_name,product_img, product_link,static_weight FROM product LEFT JOIN product_sub_category ON product.id=product_sub_category.product_id and  category=%s and product_sub_category.sub_category=%s LEFT JOIN product_style on product.id=product_style.product_id and product_style.style=%s'

    def get_main_category(self, category):
        ##main category is less than 100
        if category < 100:
            return True, category
        ## sub category
        else:
            return False, (category / 1000)

    def select_with_page(self, rows, page):
        if None == page:
            page = 1

        length = len(rows)
        beg = (int(page) - 1) * 30
        end = int(page) * 30


        if end > len(rows):
            end = len(rows)

        ret_rows = []
        for i in xrange(int(beg), int(end)):
            ret_rows.append(rows[i])

        return ret_rows
    ## return 
    def read(self, category, style=None, page=None):
        is_main_category, main_category = self.get_main_category(category)
        sql = None 
        if is_main_category and None == style:
            sql = self.main_category_sql %(main_category)
        elif is_main_category and None != style:
            sql = self.style_only_sql %(main_category, style)
        elif not is_main_category and None == style:
            sql = self.sub_category_only_sql %(main_category, category)
        elif not is_main_category and None != style:
            sql = self.sub_category_and_style_sql %(main_category, category, style)

        if None == sql:
            return None
        print 'sql:%s' %(sql)
        data_vec = self.db.query(sql)
        print 'length:%s' %(len(data_vec))
        print type(data_vec)

        return self.select_with_page(data_vec, page)

