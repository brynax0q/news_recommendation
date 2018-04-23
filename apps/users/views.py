from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View  # 继承View 完成基于类的用户登陆
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.hashers import make_password  # 对明文加密


from .models import UserProfile
from operation.models import UserWatch


class IndexView(View):
    def get(self, request):
        return render(request, "index.html")


# 基于类做用户登陆
class LoginView(View):
    # 会根据 method 调用 post或者get方法
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 从POST中取出用户名和密码
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        # 使用django.contrib.auth中authenticate方法验证用户名和密码
        user = authenticate(username=user_name, password=pass_word)
        if user is not None:      # 如果成功返回 对象，失败返回 None
            login(request, user)  # 调用login方法登陆账号

            return HttpResponse('{"msg": "成功","status": 0}', content_type='application/json')
        else:
            return HttpResponse('{"msg": "用户名或密码错误","status": 1}', content_type='application/json')


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        user_name = request.POST.get("username", "")
        if UserProfile.objects.filter(username=user_name):
            # return render(request, "register.html", {"msg": "用户已经存在"})
            return HttpResponse('{"msg": "该用户名已经存在","status": 1}', content_type='application/json')
        pass_word = request.POST.get("password", "")
        # 实例化用户，然后赋值
        user_profile = UserProfile()
        user_profile.username = user_name
        # 将明文转换为密文赋给password
        user_profile.password = make_password(pass_word)
        user_profile.save()  # 保存到数据库
        return HttpResponse('{"msg": "注册成功","status": 0}', content_type='application/json')

class LogoutView(View):
    """
    用户登出
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("login"))


class HistoryView(View):
    def get(self, request):
        user_watches = UserWatch.objects.filter(user=request.user)
        return render(request, 'history.html', {
            "user_watches": user_watches
        })
