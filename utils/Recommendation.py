# -*- coding:utf-8 -*-
__author__ = 'brynao'
__date__ = '2018/4/17 下午9:12'

import sys,os
import django
import numpy as np
sys.path.append('/Users/brynao/Desktop/code/news_recommendation')

os.chdir("/Users/brynao/Desktop/code/news_recommendation")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "news_recommendation.settings")

django.setup()

from operation.models import UserWatch
from users.models import UserProfile
from news.models import News, Init_News


News_list = News.objects.all()
has_watched = UserWatch.objects.all()



# 从用户的Model中读取所有的key，返回 key_list
def get_user_list(model):
    if model:
        user_key_list = []
        Model = eval(model)
        for tag in Model:
            for key in Model[tag]:
                user_key_list.append(key)
        return user_key_list
    print("model is empty")
    exit()

def recommendation(user_key_list):
    R_new_list = set()
    news_watched = set()
    # 统计用户已经浏览新闻的集合
    for new in has_watched:
        news_watched.add(new.new_id)

    i = 1
    for new in News_list:
        i += 1
        keys = new.keyword.split(";")
        for key in keys[0:2]:
            key = key.split(" ")[0]
            # new的关键词在用户兴趣列表中 并且 new不在用户已经浏览的集合中，则放入待推荐集合
            if key in user_key_list and new.id not in news_watched:
                R_new_list.add(new.id)
                break

    for id in R_new_list:
        new_title = News.objects.filter(id=id)
        print(new_title)

    print(len(R_new_list))
    return R_new_list


def get_cos(x,y):
    myx = np.array(x)
    myy = np.array(y)
    cos1 = np.sum(myx*myy)
    cos21 = np.sqrt(sum(myx*myx))
    cos22 = np.sqrt(sum(myy*myy))
    return cos1/float(cos21*cos22)


def compare_2(id1, id2):
    fp1 = open("/Users/brynao/Desktop/code/news_recommendation/tools/seg_article/seg_word_" + str(id1) + ".txt", "r", encoding='utf8')
    fp2 = open("/Users/brynao/Desktop/code/news_recommendation/tools/seg_article/seg_word_" + str(id2) + ".txt", "r", encoding='utf8')
    content1 = fp1.read().split()
    content2 = fp2.read().split()
    all_words = content1+content2
    test1 = {}
    test2 = {}

    for word in all_words:
        test1.setdefault(word, 0)
        test2.setdefault(word, 0)

    for word in content1:
        if word in all_words:
            test1[word] = test1[word] + 1
    for word in content2:
        if word in all_words:
            test2[word] = test2[word] + 1

    test1_v = []
    for key in test1.keys():
        test1_v.append(test1[key])
    test2_v = []
    for key in test2.keys():
        test2_v.append(test2[key])

    try:
        cos = get_cos(test1_v, test2_v)
        return cos
    except Exception as e:
        pass


def Re(user):
    for current_user in users:
        if current_user == user:
            user_watched = UserWatch.objects.all()
            cos_result = {}

            # 用户兴趣列表
            list = get_user_list(user.model)
            # 待推荐新闻id列表
            user_interest_list = recommendation(list)
            for new1 in user_interest_list:
                cos_result[new1] = 0
                for new2 in user_watched:
                    cos_result[new1] = max(compare_2(new1, new2.new_id), cos_result[new1])

            # 对结果进行排序
            cos_result = sorted(cos_result.items(), key=lambda d: d[1], reverse=True)
            # 已推荐列表
            R_lists = Init_News.objects.all()
            R_ids = set()
            for new in R_lists:
                R_ids.add(new.new_id)

            count = 0
            for item in cos_result:
                if item[0] in R_ids:
                    continue
                r = Init_News()
                r.new_id = item[0]
                r.user = user
                r.save()
                count += 1
                if count == 10:
                    break
users = UserProfile.objects.all()

# for user in users:
#     user_watched = UserWatch.objects.all()
#     cos_result = {}
#
#     # 用户兴趣列表
#     list = get_user_list(user.model)
#     # 待推荐新闻id列表
#     user_interest_list = recommendation(list)
#     print(user_interest_list)
#     for new1 in user_interest_list:
#         cos_result[new1] = 0
#         for new2 in user_watched:
#             cos_result[new1] = max(compare_2(new1, new2.new_id), cos_result[new1])
#
#     # 对结果进行排序
#     cos_result = sorted(cos_result.items(), key=lambda d: d[1], reverse=True)
#     print(cos_result)
#
#     # 已推荐列表
#     R_lists = Init_News.objects.all()
#     R_ids = set()
#     for new in R_lists:
#         R_ids.add(new.new_id)
#
#     count = 0
#     for item in cos_result:
#         if item[0] in R_ids:
#             continue
#         r = Init_News()
#         r.new_id = item[0]
#         r.user = user
#         r.save()
#         count += 1
#         if count == 10:
#             break







