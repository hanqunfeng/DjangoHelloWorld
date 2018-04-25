from django.db import models


class Book(models.Model):
    # db_column指定数据库中表的字段名称,unique=True建立唯一索引
    bookname = models.CharField('书名', max_length=50, db_column='book_name', unique=True)
    bookpapers = models.IntegerField('页数', default=0, db_column='book_papers')
    # db_index=True为该字段建立索引
    author = models.CharField('作者', max_length=20, db_column='book_author', db_index=True, default='')

    class Meta:
        db_table = "django2_book"
        app_label = "django2"

    def __str__(self):
        return self.bookname

    def get(self, attr):
        if attr == 'id':
            return self.id
        if hasattr(self, attr):
            return getattr(self, attr)
        else:
            return None
