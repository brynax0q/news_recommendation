from django.shortcuts import render
from django.views.generic.base import View
from .models import News, Init_News
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from operation.models import UserWatch
from users.models import UserProfile
from django.http import HttpResponse
from datetime import datetime
import threading

from utils.compute_model import *
from utils.Recommendation import Re

t = {
    "politics": "时政",
    "legal": "法制",
    "fortune": "经济",
    "mil": "军事",
    "local": "地方",
    "food": "食物",
    "tech": "科技",
    "house": "房产",
    "re": "推荐",
}

class NewListView(View):
    def get(self, request):

        print(request.user)

        all_news = News.objects.all().order_by("-create_time")
        all_num = all_news.count()

        legal_news = all_news.filter(tag="法制")
        legal_num = legal_news.count()

        politics_news = all_news.filter(tag="时政")
        politics_num = politics_news.count()

        fortune_news = all_news.filter(tag="经济")
        fortune_num = fortune_news.count()

        mil_news = all_news.filter(tag="军事")
        mil_num = mil_news.count()

        tech_news = all_news.filter(tag="科技")
        tech_num = tech_news.count()

        local_news = all_news.filter(tag="地方")
        local_num = local_news.count()

        house_news = all_news.filter(tag="房产")
        house_num = house_news.count()

        food_news = all_news.filter(tag="食物")
        food_num = food_news.count()

        all_re_news = Init_News.objects.all().order_by("id")
        if request.user.is_authenticated():
            re_news = all_re_news.filter(user=request.user)
            re_num = re_news.count()
        else:
            re_num = 0
            re_news = {}

        type = request.GET.get('type', "")
        if type == '':
            all_news = all_news
        elif type == 're':
            all_news = re_news
        else:
            all_news = all_news.filter(tag=t[type])

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_news, 20, request=request)

        all_news = p.page(page)

        return render(request, 'index.html',{
            "all_news": all_news,
            "all_num": all_num,

            "politics_news": politics_news,
            "legal_news": legal_news,
            "fortune_news": fortune_news,
            "mil_news": fortune_news,
            "tech_news": tech_news,
            "local_news": local_news,
            "house_news": house_news,
            "food_news": food_news,

            "politics_num": politics_num,
            "fortune_num": fortune_num,
            "mil_num": mil_num,
            "tech_num": tech_num,
            "legal_num": legal_num,
            "local_num": local_num,
            "house_num": house_num,
            "food_num": food_num,
            "re_num": re_num,
            "type": type
        })

class PageView(View):
    def get(self, request, new_id):
        new = News.objects.get(id=int(new_id))
        new.click_nums += 1
        new.save()

        if request.user.is_authenticated():
            # 查询登录用户是否已经阅读了这个新闻
            user_watches = UserWatch.objects.filter(user=request.user, new=new)
            if not user_watches:
                # 添加浏览历史记录
                user_watch = UserWatch(user=request.user, new=new, id=int(new_id))

                # 更新用户兴趣关键字
                t = threading.Thread(target=updataUserModel(user_watch)).start()
                # updataUserModel(user_watch)
                user_watch.save()
            else:
                user_watches.update(add_time=datetime.now())
        return render(request, "page.html", {
            "new": new,
        })

class ReView(View):
    def post(self, request):
        # 判断用户是否登陆
        if not request.user.is_authenticated():
            return HttpResponse('{"status": "fail", "msg":"用户未登录"}', content_type='application/json')
        print(request.user)
        threading.Thread(target=Re(request.user)).start()
        return HttpResponse('{"status": "success", "msg":"收藏"}', content_type='application/json')
