from django.db import connection
from django.test import Client
from django.test import TestCase

from myapp.models.car import Car
from myapp.models.user import User
from myapp.utils import dbutils
from utils import XMLUtil, JSONUtil


# Create your tests here.

class UserTests(TestCase):
    client = None

    @classmethod
    def setUpClass(cls):  # 测试前执行
        ua = User.objects.create(name="yyyyy")
        ub = User.objects.create(name="qqqqq")
        uc = User.objects.create(name="aaaaa")
        ca = Car.objects.create(carNum='aaaaaa', carColor=1, carPrice=12.22)
        ca.user.add(ua, ub)
        cb = Car.objects.create(carNum='bbbbbb', carColor=1, carPrice=22.22)
        cb.user.add(uc, ua)
        cc = Car.objects.create(carNum='cccccc', carColor=1, carPrice=33.22)
        cc.user.add(ua)
        cls.client = Client()

        super().setUpClass()

    @classmethod
    def tearDownClass(cls):  # 测试后执行
        super().tearDownClass()

    # def test_user_save(self):
    #     s = requests.session()
    #     print(s.headers)
    #     url = "http://127.0.0.1:8000/myapp/users/save/"
    #
    #     postdata = {"name": "测试用户"}
    #
    #     r = requests.post(url, data=postdata)
    #
    #     print(r.status_code)
    #     print(r.content)
    #     print(r.request)

    def test_user_save(self):
        postdata = {'name': '测试用户', 'birth_day': '2011-01-01', 'phone': '123123123123', 'email': '123@123.com'}
        response = self.client.post('/myapp/users/save/', postdata, follow=True)
        print(response.redirect_chain)
        print(response.status_code)
        print(response.content)
        print(User.objects.all())

    def test_get_users_json(self):
        response = self.client.get('/myapp/users/json/')
        print('==================test_get_user_json start=======================')
        print(response.status_code)
        # print(response.content)
        print(response.json())
        print('==================test_get_user_json end=======================')

    def test_sql(self):
        print("1==================================")
        users = User.objects.values('id', 'name')
        for u in users:
            print(u)
        print("2==================================")
        users = User.objects.raw('select id,name from sys_user ')
        for u in users:
            print(u)
        print("3==================================")

    def test_sql_connection(self):
        with connection.cursor() as cursor:
            cursor.execute("select id,name from sys_user")
            users = cursor.fetchall()

        for u in users:
            print(u)

    def test_sql_connection2(self):
        with connection.cursor() as cursor:
            cursor.execute("select id,name from sys_user")
            users = dbutils.dictfetchall(cursor)

        for u in users:
            print(u)

    def test_sql_connection3(self):
        with connection.cursor() as cursor:
            cursor.execute("select id,name from sys_user")
            users = dbutils.namedtuplefetchall(cursor)

        for u in users:
            print(u)

    def test_aggregate(self):
        from django.db.models import Avg, Max, Min, FloatField
        avg_price = Car.objects.all().aggregate(Avg('carPrice'))  # 这里all()可以没有，这里结果字典中的key是自动生成的
        print("avg_price==", avg_price)  # avg_price== {'carPrice__avg': 22.553333}
        avg_price = Car.objects.aggregate(
            price_avg=Avg('carPrice'))  # 这里all()可以没有，如果希望自定义这个key，可以为其指定price_avg=Avg('carPrice')
        print("avg_price==", avg_price)  # avg_price== {'price_avg': 22.553333}
        max_price = Car.objects.all().aggregate(Max('carPrice'))
        print("max_price==", max_price)  # max_price== {'carPrice__max': Decimal('33.22')}
        max_price = Car.objects.all().aggregate(Max('carPrice', output_field=FloatField()))
        print("max_price==", max_price)  # max_price== {'carPrice__max': 33.22}
        # 注意这里要给计算内容起一个别名，否则结果字典不知道key是什么
        price_diff = Car.objects.aggregate(price_diff=Max('carPrice', output_field=FloatField()) - Avg('carPrice'))
        print("price_diff==", price_diff)  # price_diff== {'price_diff': 10.666667}
        print(price_diff['price_diff'])  # 10.666667

        aggreate = Car.objects.aggregate(Avg('carPrice'), Max('carPrice'), Min('carPrice'))
        print("aggreate==", aggreate)

        avg_price_gte20 = Car.objects.filter(carPrice__gte=20).aggregate(Avg('carPrice'))
        print("avg_price_gte20==", avg_price_gte20)

    def test_annotate(self):
        from django.db.models import Count, Min, Max
        # 为每个car对象增加额外的属性，这里增加的是用户数量，定义属性名称为num_users
        cars = Car.objects.annotate(num_users=Count('user'))
        for car in cars:
            print(car.num_users)

        cars = Car.objects.filter(carPrice__gte=20).annotate(num_users=Count('user'))
        for car in cars:
            print(car.num_users)

        # 因为每一个annotate后都是一个QuerySet，所以可以组合filter方法，先设置属性，然后对属性进行过滤
        cars = Car.objects.filter(carPrice__gte=20).annotate(num_users=Count('user')).filter(num_users__gte=2)
        for car in cars:
            print(car.num_users)

        # 设置关联对象属性，注意管理对象属性使用双下划线
        users = User.objects.annotate(car_min_price=Min('car__carPrice'), car_max_price=Max('car__carPrice'))
        for user in users:
            print(user.id, '--', user.name, 'min$', user.car_min_price, 'max$', user.car_max_price)

    def test_xml(self):
        print("==============test_xml start==================")
        user_list = User.objects.all()
        xml = XMLUtil.to_xml(user_list)
        print(xml)

        objectList = XMLUtil.xml_to_list(xml)
        print(objectList)
        for object in objectList:
            print(object)
            print(object.name)
        print("==============test_xml end==================")

    def test_json(self):
        print("==============test_json start==================")
        user_list = User.objects.filter(pk=1)
        json = JSONUtil.to_json(user_list)
        print(json)

        user_list = JSONUtil.json_to_list(json)
        print(user_list)
        for user in user_list:
            print(user)

        print("==============test_json end==================")
