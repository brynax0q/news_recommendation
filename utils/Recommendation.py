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
                if float(Model[tag][key]) > 0.1:
                    user_key_list.append(key)
        return user_key_list
    print("model is empty")
    exit()

def get_user_dict(model):
    if model:
        user_key_list = {}
        Model = eval(model)
        for tag in Model:
            for key in Model[tag]:
                if float(Model[tag][key]) > 0.1:
                    user_key_list[key] = Model[tag][key]
        return user_key_list
    print("model is empty")
    exit()

def recommendation(user_key_list):
    R_new_list = set()
    news_watched = set()

    list = dict(user_key_list)

    print("初始兴趣列表",list)

    user_key_list = list.keys()
    result_list = {}
    # 统计用户已经浏览新闻的集合
    for new in has_watched:
        news_watched.add(new.new_id)

    for new in News_list:
        keys = new.keyword.split(";")
        # 　　　keys 是每一个新闻的关键词列表
        for key in keys[0:5]:
            key = key.split(" ")[0]

            # new的关键词在用户兴趣列表中 并且 new不在用户已经浏览的集合中，则放入待推荐集合
            if key in user_key_list and new.id not in news_watched:
                # R_new_list.add(new.id)
                result_list[key] = result_list.setdefault(key, 0) + 1
                break

    result_list = sorted(result_list.items(), key=lambda d: d[1], reverse=False)


    result_list = dict(result_list)

    result_list = {key: value for key, value in result_list.items() if value != 1}
    print("个数统计",result_list)

    sum = 0
    for item in result_list:
        sum += result_list[item]
    if len(result_list) == 1:
        ave = 0
    else:
        ave = sum/len(result_list)

    sum = 0
    for item in result_list:
        sum += (result_list[item]-ave)**2
    if len(result_list) == 1:
        o = 1
    else:
        o = (sum/len(result_list))**(1/2)

    for item in result_list:
        result_list[item] = abs((float(result_list[item]) - ave)/o) * float(list[item])

    result_list = dict(sorted(result_list.items(), key=lambda d: d[1], reverse=True))
    # for id in R_new_list:
    #     new_title = News.objects.filter(id=id)
    #     print(new_title)
    #
    # print(len(R_new_list))
    sum = 0
    for item in result_list:
        sum += result_list[item]

    for item in result_list:
        result_list[item] = int((result_list[item] / sum) * 100)
    print("调整个数",result_list)

    result_list_key = result_list.keys()

    for new in News_list:
        keys = new.keyword.split(";")
        # 　　　keys 是每一个新闻的关键词列表
        for key in keys[0:5]:
            key = key.split(" ")[0]

            # new的关键词在用户兴趣列表中 并且 new不在用户已经浏览的集合中，则放入待推荐集合
            if key in result_list_key and new.id not in news_watched and result_list[key] > 0:
                R_new_list.add(new.id)
                result_list[key] -= 1
                break


    return R_new_list


def get_cos(x,y):
    myx = np.array(x)
    myy = np.array(y)
    cos1 = np.sum(myx*myy)
    cos21 = np.sqrt(sum(myx*myx))
    cos22 = np.sqrt(sum(myy*myy))
    return cos1/float(cos21*cos22)

def compare_by_kw(id1, id2):
    fp1 = News.objects.get(id=id1)
    fp2 = News.objects.get(id=id2)
    kws1 = fp1.keyword.split(";")
    kws2 = fp2.keyword.split(";")
    content1 = []
    content2 = []
    for kw in kws1[:5]:
        content1.append(kw.split()[0])
    for kw in kws2[:5]:
        content2.append(kw.split()[0])
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
    count = 0
    users = UserProfile.objects.all()
    for current_user in users:
        if current_user == user:
            user_watched = UserWatch.objects.all()
            cos_result = {}

            # 用户兴趣列表
            # list = get_user_list(user.model)
            list = get_user_dict(user.model)
            list = sorted(list.items(), key=lambda d: d[1], reverse=True)
            # 待推荐新闻id列表
            user_interest_list = recommendation(list)

            # i = 1
            # for new1 in user_interest_list:
            #     cos_result[new1] = 0
            #     for new2 in user_watched:
            #         # cos_result[new1] = max(compare_2(new1, new2.new_id), cos_result[new1])
            #         cos_result[new1] = max(compare_by_kw(new1, new2.new_id), cos_result[new1])
            #         print(i)
            #         i += 1
            #
            # # 对结果进行排序
            # cos_result = sorted(cos_result.items(), key=lambda d: d[1], reverse=True)

            # 已推荐列表
            R_lists = Init_News.objects.all()
            R_ids = set()
            for new in R_lists:
                R_ids.add(new.new_id)

            for id in user_interest_list:
                if id in R_ids:
                    continue
                r = Init_News()
                r.new_id = id
                r.user = user
                r.save()
                count += 1
                if count == 100:
                    break


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







