import datetime

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils import timezone

# 自定义文件存储路径及web访问路径
fs = FileSystemStorage(location='/Users/hanqunfeng/python_workspace/FILE/', base_url='http://localhost/files/')


# Create your models here.

# 在这个简单的投票应用中，我们将创建两个模型： Question和Choice。
# Question对象具有一个question_text（问题）属性和一个publish_date（发布时间）属性。
# Choice有两个字段：选择的内容和选择的得票统计。 每个Choice与一个Question关联
class Question(models.Model):
    question_text = models.CharField(max_length=200)  # 字符字段，并且限制最大长度为200
    pub_date = models.DateTimeField('date published')  # 日期字段，第一个字符串参数用于定义人类可读的名字
    photo = models.ImageField(upload_to="photo", default="default/django.jpeg")  # 路径相对于MEDIA_ROOT的配置
    uploadfile = models.FileField(upload_to="file", storage=fs, default="")

    def __str__(self):
        return self.question_text

    # 判断是否为最近1天之内发布的,timedelta()表示时间间隔
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 外键关联，并且设置为级联删除
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)  # 整型字段，并且设置缺省值为0

    def __str__(self):
        return self.choice_text
