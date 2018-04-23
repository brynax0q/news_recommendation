from django.db import models

from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name=u'昵称')
    birth = models.DateField(verbose_name=u'生日', null=True, blank=True)
    mobile = models.CharField(max_length=11, null=True, blank=True)
    model = models.TextField(verbose_name='用户兴趣模型', null=True, blank=True)

    class Mate:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

