from django.db import models
from users.models import UserProfile
from news.models import News
from datetime import datetime

class UserWatch(models.Model):
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", null=True, blank=True)
    new = models.ForeignKey(News, verbose_name=u"新闻", null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = "用户浏览记录"
        verbose_name_plural = verbose_name
