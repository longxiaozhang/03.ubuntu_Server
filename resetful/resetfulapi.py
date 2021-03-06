# -*- coding:utf8 -*-
import time
from flask import Flask,g,request,render_template,request,flash,url_for,make_response,g,redirect

from database.datamodule import before_request_handler,after_request_handler,tb_movies,tb_links,tb_doubans
from resetfulutils import *
import json


apiapp = Flask(__name__)
apiapp.secret_key = 'some_secret'

MAX_NUM = 60
def startresetful(port):
    print "启动电影的api %s" %port
    apiapp.run(host='0.0.0.0',port=port)

@apiapp.before_request
def before_request():
    before_request_handler()


@apiapp.teardown_request
def teardown_request(exception):
    after_request_handler()

# 查找最近更新的电影
@apiapp.route('/movies/new_update_movies/',methods= ['GET'])
def new_update_movies_count():
    if request.method == "GET":
        data = [dic for dic in tb_movies.select(tb_movies,tb_doubans).join(tb_doubans).order_by(tb_movies.updatetime.desc()).limit(MAX_NUM).dicts()]
        return make_jsonresponse(data)
# 查找最近更新的电影
@apiapp.route('/movies/new_update_movies/<count>',methods= ['GET'])
def new_update_movies(count):
    if request.method == "GET":
        data = [dic for dic in tb_movies.select(tb_movies,tb_doubans).join(tb_doubans).order_by(tb_movies.updatetime.desc()).limit(count).dicts()]
        return make_jsonresponse(data)

# 查找某年的电影
@apiapp.route('/movies/year/<year>',methods= ['GET'])
def new_movies(year):
    if request.method == "GET":
        q = tb_movies.select(tb_movies,tb_doubans).join(tb_doubans).where(tb_doubans.year == year).order_by(tb_doubans.rating.desc()).limit(MAX_NUM).dicts()
        data = [dic for dic in q]
        return make_jsonresponse(data)
# 查找所有年份
@apiapp.route('/movies/years/',methods = ['GET'])
def get_years():
    if request.method == "GET":
        q = tb_doubans.select(tb_doubans.year).group_by(tb_doubans.year).order_by(tb_doubans.year.desc()).dicts()

        data = [dic for dic in q]

        return make_jsonresponse(data)

# 查找种类
@apiapp.route('/movies/cate/<cate>',methods = ['GET'])
def cate_movies(cate):
    if request.method == "GET":
        if cate == 'science':
            q = tb_movies.select(tb_movies,tb_doubans).join(tb_doubans).where(tb_movies.cate.contains('科幻')).order_by(tb_doubans.rating.desc()).limit(MAX_NUM).dicts()
            data = [dic for dic in q]

            return make_jsonresponse(data)


@apiapp.route('/movies/',methods = ['GET'])
def searchall():
    if request.method == "GET":
        data = [dic for dic in tb_movies.select(tb_movies,tb_doubans).join(tb_doubans).dicts()]
        return make_jsonresponse(data)

# 查找某个名字的电影
@apiapp.route('/movies/name/<name>',methods = ['GET','POST'])
def search(name):
    if request.method == "GET":
        data = [dic for dic in tb_movies.select(tb_movies,tb_links).join(tb_links).where(tb_movies.name.contains(name)).limit(MAX_NUM).dicts()]
        return make_jsonresponse(data)
    else:
        pass

# 通过id查找link信息
@apiapp.route('/movies/link/<id>')
def links(id):
    if request.method == "GET":
        data = [dic for dic in tb_links.select().where(tb_links.movie == id).dicts()]
        return make_jsonresponse(data)
    else:
        pass

@apiapp.route('/movies/<linkid>/download/',methods = ['GET','POST'])
def localpaths(linkid):
    if request.method == "GET":
        download_task(linkid)
        return make_jsonresponse("")
    else:
        pass

@apiapp.route('/movies/download/',methods = ['GET'])
def remotepaths():
    if request.method == "GET":
        data = [dic for dic in tb_links.select().where(tb_links.gid != "").dicts()]
        return make_jsonresponse(data)
    else:
        pass
    pass


def make_jsonresponse(data):
    json_response = json.dumps(data, indent=4, sort_keys=False, ensure_ascii=False)
    response = make_response(json_response)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET'
    response.headers['Access-Control-Max-Age'] = '60'
    response.headers['Access-Control-Allow-Headers']='x-requested-with,content-type'
    return response