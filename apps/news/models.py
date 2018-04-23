from django.db import models
from users.models import UserProfile

class News(models.Model):
    url = models.CharField(max_length=150, verbose_name="链接", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name='标题', null=True, blank=True)
    tag = models.CharField(verbose_name="新闻标签", max_length=5)
    abstract = models.CharField(max_length=500, verbose_name='概述')
    keyword = models.CharField(max_length=100, verbose_name='关键字')
    content = models.TextField(verbose_name='正文', null=True, blank=True)
    click_nums = models.IntegerField(verbose_name='点击次数', null=True, blank=True, default=0)
    create_time = models.DateTimeField(verbose_name='时间')

    class Meta:
        verbose_name = '新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Init_News(models.Model):
    new = models.ForeignKey(News, verbose_name=u"新闻", null=True, blank=True)
    user = models.ForeignKey(UserProfile, verbose_name=u"用户", null=True, blank=True)

    class Meta:
        verbose_name = '推荐新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.new.title