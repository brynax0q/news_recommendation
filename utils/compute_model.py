# -*- coding:utf-8 -*-
__author__ = 'brynao'
__date__ = '2018/4/17 下午9:09'

def updataUserModel(user_watch):
    # 获取本次浏览的 新闻type、新闻关键字

    new_tag = user_watch.new.tag
    new_kw = user_watch.new.keyword

    # 将新闻关键字转为dict
    tmp_kw = {}
    new_kw = new_kw.split(";")
    for item in new_kw[:-1]:
        item = item.split(" ")
        tmp_kw[item[0]] = item[1]

    # 获取用户的 兴趣模型
    user_Model = user_watch.user.model
    # 如果模型为空
    if user_Model == '' or user_Model == None:
        Model = {}
    else:
        Model = eval(user_Model)

    # 如果本次访问的新闻类型不在model中
    if(Model.get(new_tag) is None):
        Model[new_tag] = tmp_kw
        user_watch.user.model = Model
    # 本次访问的新闻类型在model中
    else:
        m_keys = Model[new_tag].keys()
        t_keys = tmp_kw.keys()
        for t in t_keys:
            if t in m_keys:
                Model[new_tag][t] = str(float(Model[new_tag][t]) + float(tmp_kw[t]))
            else:
                Model[new_tag][t] = tmp_kw[t]

    user_watch.user.model = Model
    user_watch.user.save()
    # 本次访问的新闻页面类型在model中