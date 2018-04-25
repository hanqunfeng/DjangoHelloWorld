from django.db import connections
from django.test import TestCase

from django2.models.book import Book


# Create your tests here.

class Django2Test(TestCase):

    @classmethod
    def setUpClass(cls):  # 测试前执行
        Book.objects.create(bookname='西游记', bookpapers=10000)
        Book.objects.create(bookname='红楼梦', bookpapers=20000)
        Book.objects.create(bookname='水浒传', bookpapers=30000)
        Book.objects.create(bookname='三国演义', bookpapers=40000)
        super().setUpClass()

    @classmethod
    def tearDownClass(cls):  # 测试后执行
        super().tearDownClass()

    def test_sql(self):
        with connections['django2_db'].cursor() as cursor:
            cursor.execute("select id,book_name,book_papers from django2_book")
            books = cursor.fetchall()

        for b in books:
            print(b)
