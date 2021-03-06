#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import defaultdict

import web

import config
import model as m
import sys
import http_driver 
import json
import time
import datetime
import data_read
import string
import random

reload(sys)
sys.setdefaultencoding('utf-8')

VERSION = "0.0.1"

urls = (
    r'/', 'Tech',
    r'/technology/\d+', 'Tech',
    r'/think/\d+', 'Think',
    r'/startup/\d+', 'Startup',
    ##r'/decorations/\d+', 'Decorations',
    r'/(.*)', 'static_get',
    )

app = web.application(urls, globals())

# Allow session to be reloadable in development mode.
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
                                  initializer={'flash': defaultdict(list)})

    web.config._session = session
else:
    session = web.config._session


def flash(group, message):
    session.flash[group].append(message)


def flash_messages(group=None):
    if not hasattr(web.ctx, 'flash'):
        web.ctx.flash = session.flash
        session.flash = defaultdict(list)
    if group:
        return web.ctx.flash.get(group, [])
    else:
        return web.ctx.flash

render = web.template.render('templates/',
                             base='base',
                             cache=config.cache)
t_globals = web.template.Template.globals
t_globals['datestr'] = web.datestr
t_globals['app_version'] = lambda: VERSION + ' - ' + config.env
t_globals['flash_messages'] = flash_messages
t_globals['render'] = lambda t, *args: render._template(t)(*args)

class Common:
    def notice_log(self, path, param):
        ts=int(time.time())
        d = datetime.datetime.fromtimestamp(ts)
        timestamp = d.strftime("%Y-%m-%d %H:%M:%S")

        cookie_value = self.get_cookie()

        config.logger.info("[%s][%s][%s][%s][%s]" %(timestamp, self.ip, cookie_value, path, param))

    def generate_id(self):
        l = [str(x) for x in string.digits]
        random.shuffle(l)
        return ''.join(l)

    def set_cookie(self):
        c_n = 'c_raintoo'
        c_v = self.generate_id()
        web.setcookie(c_n, c_v)
        return c_v

    def get_cookie(self):
        c=web.cookies(c_raintoo='000')
        c_v = c.c_raintoo
        if c_v == '000':
            c_v = self.set_cookie()
            config.logger.info('set_cookie:%s', c_v)
        else:
            config.logger.info('get_cookie:%s', c_v)

        return c_v

class static_get(Common):
    def GET(self, file):
        cookie_value = self.get_cookie()
        config.logger.info('user:%s access file:%s', cookie_value, file)
        web.seeother('/static/'+file)

class Startup(Common):
    def __init__(self):

        self.ip = '127.0.0.1'

        #self.product_db = ProductDb()

    def GET(self):
        #flash("success", """Welcome! Application code lives in app.py,
        #models in model.py, tests in test.py, and seed data in seed.py.""")
        self.ip = web.ctx['ip']
        path = web.ctx['path']
        param = web.input()

        self.notice_log("path:%s" %(path), "param:%s" %(param))
        
        path_vec = path.split('/')
        if len(path_vec) < 2:
            return None
        category = path_vec[2]

        page = None
        style = None
        if len(param) > 0:
            if 'page' in param:
                page = param['page']
            if 'style' in param:
                style = param['style']

        dr = data_read.DataReader()
        print 'category:%s' %(category)
        print 'style:%s' %(style)
        print 'page:%s' %(page)

        if None == page or 0==int(page):
            page = 1
        input_rows = dr.read(int(category), style, page)

        matrix = []
        
        num_in_row = 2
        cur_num = 0

        view_row = []
        for ele in input_rows:
            e = {}
            e['desc'] = ele['product_name'] 
            e['img'] = '/static/product_images/' + ele['product_img']
            e['link'] = ele['product_link']

            view_row.append(e)

            if (cur_num + 1) % num_in_row == 0:
                matrix.append(view_row)
                view_row = []
            cur_num = cur_num + 1

        if len(view_row) !=  0:
            matrix.append(view_row)

        return render.startup(matrix, int(page))

class Tech(Common):
    def __init__(self):

        self.ip = '127.0.0.1'

        #self.product_db = ProductDb()

    def GET(self):
        #flash("success", """Welcome! Application code lives in app.py,
        #models in model.py, tests in test.py, and seed data in seed.py.""")
        self.ip = web.ctx['ip']
        path = web.ctx['path']
        param = web.input()

        self.notice_log("path:%s" %(path), "param:%s" %(param))
        
        path_vec = path.split('/')
        category = 10

        if len(path_vec) >= 3:
            category = path_vec[2]

        page = None
        style = None
        if len(param) > 0:
            if 'page' in param:
                page = param['page']
            if 'style' in param:
                style = param['style']

        dr = data_read.DataReader()

        if None == page or 0==int(page):
            page = 1

        input_rows = dr.read(int(category), style, page)

        matrix = []
        
        num_in_row = 2
        cur_num = 0

        view_row = []
        for ele in input_rows:
            e = {}
            e['desc'] = ele['product_name'] 
            e['img'] = '/static/product_images/' + ele['product_img']
            e['link'] = ele['product_link']

            view_row.append(e)

            if (cur_num + 1) % num_in_row == 0:
                matrix.append(view_row)
                view_row = []
            cur_num = cur_num + 1

        if len(view_row) !=  0:
            matrix.append(view_row)

        return render.technology(matrix, int(page))


class Think(Common):
    def __init__(self):

        self.ip = '127.0.0.1'

        #self.product_db = ProductDb()

    def GET(self):
        #flash("success", """Welcome! Application code lives in app.py,
        #models in model.py, tests in test.py, and seed data in seed.py.""")
        self.ip = web.ctx['ip']
        path = web.ctx['path']
        param = web.input()

       # print "path is:%s" %(path)
        #ret = self.get_env()

        self.notice_log("path:%s" %(path), "param:%s" %(param))
        
        path_vec = path.split('/')
        if len(path_vec) < 2:
            return None
        category = path_vec[2]

        page = None
        style = None
        if len(param) > 0:
            if 'page' in param:
                page = param['page']
            if 'style' in param:
                style = param['style']

        dr = data_read.DataReader()
        print 'category:%s' %(category)
        print 'style:%s' %(style)
        print 'page:%s' %(page)

        if None == page or 0==int(page):
            page = 1
        input_rows = dr.read(int(category), style, page)

        matrix = []
        
        num_in_row = 2
        cur_num = 0

        view_row = []
        for ele in input_rows:
            e = {}
            e['desc'] = ele['product_name'] 
            e['img'] = '/static/product_images/' + ele['product_img']
            e['link'] = ele['product_link']

            view_row.append(e)

            if (cur_num + 1) % num_in_row == 0:
                matrix.append(view_row)
                view_row = []
            cur_num = cur_num + 1

        if len(view_row) !=  0:
            matrix.append(view_row)

        return render.think(matrix, int(page))

# Set a custom internal error message
def internalerror():
    msg = """
    An internal server error occurred. Please try your request again by
    hitting back on your web browser. You can also <a href="/"> go back
     to the main page.</a>
    """
    return web.internalerror(msg)


# Setup the application's error handler
app.internalerror = web.debugerror if web.config.debug else internalerror

if config.email_errors.to_address:
    app.internalerror = web.emailerrors(config.email_errors.to_address,
                                        app.internalerror,
                                        config.email_errors.from_address)


# Adds a wsgi callable for uwsgi
application = app.wsgifunc()
if __name__ == "__main__":
    app.run()
