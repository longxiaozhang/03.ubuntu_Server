# -* - coding: UTF-8 -* -
from common.config import *

import datetime
from peewee import *
from playhouse.sqlite_ext import SqliteExtDatabase

DATABASE = getmoviedb()

database_object = SqliteDatabase(DATABASE)

def create_table():
    database_object.create_table(tb_links,safe=True)
    database_object.create_table(tb_movies,safe=True)
    database_object.create_table(tb_doubans,safe=True)
    database_object.create_table(tb_downloads,safe=True)

def before_request_handler():
    database_object.connect()

def after_request_handler():
    database_object.close()

class BaseModel(Model):
    class Meta:
        database = database_object



class tb_movies(BaseModel):
    id = IntegerField(primary_key=True)
    org_url = TextField(default=u'')
    title =TextField(default=u'')
    name = TextField(default=u'')
    cate = TextField(default=u'')
    updatetime = TextField(default=datetime.datetime.now().strftime(u"%Y-%m-%d"))
    img = TextField(default=u'')
    #douban = ForeignKeyField(tb_doubans,related_name='douban')

class tb_subscript(BaseModel):
    id = IntegerField(primary_key=True)

class tb_doubans(BaseModel):
    id = IntegerField(primary_key=True)
    title = TextField(default=u'')
    #original_title = TextField(default=u'')
    douban_url = TextField(default=u'')
    rating = TextField(default=u'')
    directors = TextField(default=u'')
    genres = TextField(default=u'')
    pubdates = TextField(default=u'')
    year = TextField(default=u'')
    rating_betterthan = TextField(default=u'')
    movie = ForeignKeyField(tb_movies)


class tb_links(BaseModel):
    id = IntegerField(primary_key=True)
    movie = ForeignKeyField(tb_movies)

    gid = TextField(default=u'')
    status = TextField(default=u'')
    sourceurl=TextField(default=u'')
    downloadpath = TextField(default=u'')
    playpath = TextField(default=u'')
    dir = TextField(default=u'')
    completedLength = TextField(default=u'')
    downloadSpeed =TextField(default=u'')
    errorMessage = TextField(default=u'')
    totalLength = TextField(default=u'')

class tb_downloads(BaseModel):
    id = IntegerField(primary_key=True)
    link = ForeignKeyField(tb_links)

class testdb(BaseModel):
    id = IntegerField(primary_key=True)
    name = TextField(default=u'')

