# -*- coding:utf-8 -*-
__author__ = 'brynao'
__date__ = '2017/11/16 下午4:28'


import xadmin
from .models import News

class NewsAdmin(object):
    list_display = ['title', 'desc', 'body', 'click_nums', 'tag']
    search_fields = ['title', 'desc', 'body', 'click_nums', 'tag']
    list_filter = ['title', 'desc', 'body', 'click_nums', 'tag']
    readonly_fields = ['click_nums']


xadmin.site.register(News, NewsAdmin)