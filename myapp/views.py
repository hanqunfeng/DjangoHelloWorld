import datetime
import time

from django.core.cache import caches
from django.db import transaction
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods, require_GET

from .libraries import utils
from .models.car import Car
from .models.identity_card import IdentityCard
from .models.user import User

cache = caches['default']


# Create your views here.

@require_GET  # 只接受get请求 == @require_http_methods(["GET"])，@require_POST 只接受post请求
def user_index(request):
    user_list = cache.get('user_list')
    if not user_list:
        user_list = User.objects.order_by('-id')[:10]
        cache.set('user_list', user_list)
    # Q对象用于封装查询条件，功能更强大，支持OR(|)和AND(,)，同时支持NOT(~)
    # filter只支持AND，所以可以组合使用Q对象和fiter方法来实现复杂查询
    # exclude()方法同filter方法，等同于Q对象的NOT(~)，即排除过滤条件:filter(~Q(email="None")) ===== exclude(email="None")
    # user_list = User.objects.filter(
    #     Q(name__isnull=False), Q(email__endswith="163.com") | Q(phone="None") | Q(phone__isnull=True),
    # ).filter(email__isnull=False).filter(~Q(email="None")).order_by('-id')[:10]

    context = {'user_list': user_list}

    return render(request, 'myapp/user/index.html', context)


def user_index_query(request, year=None, name=None):
    # Q对象用于封装查询条件，功能更强大，支持OR(|)和AND(,)，同时支持NOT(~)
    # filter只支持AND，所以可以组合使用Q对象和fiter方法来实现复杂查询
    # exclude()方法同filter方法，等同于Q对象的NOT(~)，即排除过滤条件:filter(~Q(email="None")) ===== exclude(email="None")
    user_list = User.objects
    if year:
        user_list = user_list.filter(birth_day__year=year)
    if name:
        user_list = user_list.filter(name__contains=name)
    user_list = user_list.order_by('-id')[:10]
    context = {'user_list': user_list}
    return render(request, 'myapp/user/index.html', context)


def user_detail(request, user_id):
    if user_id == 0:
        user = None  # 此时就会给出新的ID,并发时不可以这样处理
    else:
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404("user does not exist")  # 没有查询到数据则抛出404异常
    return render(request, 'myapp/user/detail.html', {'user': user})


# 只允许接收post请求
@require_http_methods(["POST"])  # @require_http_methods(["POST","GET"]) 同时支持get和post
# 关闭csrf验证
@csrf_exempt
@transaction.atomic  # 开启事务
def user_save(request):
    # id = request.POST['id'] #这种方式取参数，当参数不存在时会报错，推荐使用下面的方式获取参数，并设置默认值
    id = request.POST.get('id', None)  # id参数不存在时设置为None
    if id:
        user = User.objects.get(pk=id)
        identitycard = user.identitycard
    else:
        user = User.objects.create()
        identitycard = IdentityCard.objects.create(user=user)

    name = request.POST.get('name', None)
    birth_day = request.POST.get('birth_day', None)
    phone = request.POST.get('phone', None)
    email = request.POST.get('email', None)

    if birth_day and birth_day != "None":
        # % a
        # 英文星期简写 'Sun'
        # % A
        # 英文星期的完全 'Sunday'
        # % b
        # 英文月份的简写 'Sep'
        # % B
        # 英文月份的完全 'September'
        # % c
        # 显示本地日期时间 '09/15/13 21:43:29'
        # % d
        # 日期，取1 - 31
        # % H
        # 小时， 0 - 23;
        # % I
        # 小时， 0 - 12;
        # % m
        # 月， 01 - 12;
        # % M
        # 分钟，1 - 59
        # % S
        # 显示0 - 59之间的秒数
        # % j
        # 年中当天的天数
        # % w
        # 显示今天是星期几，星期天为0，星期一为1
        # % W
        # 显示一年中的第几周，星期一为一周的第一天
        # % U
        # 显示一年中的第几周，星期天为一周的第一天
        # % p
        # 以 A.M./P.M.方式显示是上午还是下午 'PM'
        # % x
        # 本地的当天日期 '09/17/13'
        # % X
        # 本地的当天时间 '07:55:04'
        # % y
        # 年份
        # 00 - 99;
        # % Y
        # 年份的完整拼写
        # 例子:显示当前日期时间：格式为：年-月-日 时:分:秒
        # '%Y-%m-%d %H:%M:%S'  '2013-09-17 08:06:17'
        y, m, d = time.strptime(birth_day, "%Y-%m-%d")[0:3]
        birth_day = datetime.datetime(y, m, d)
        user.birth_day = birth_day
    if name and name != "None":
        user.name = name
    if phone and phone != "None":
        user.phone = phone
    if email and email != "None":
        user.email = email

    cardId = request.POST.get('cardId', None)
    address = request.POST.get('address', None)
    issuing_organ = request.POST.get('issuing_organ', None)
    validity_date = request.POST.get('validity_date', None)

    if cardId and cardId != "None":
        identitycard.cardId = cardId
    if address and address != "None":
        identitycard.address = address
    if issuing_organ and issuing_organ != "None":
        identitycard.issuing_organ = issuing_organ
    if validity_date and validity_date != "None":
        y, m, d = time.strptime(validity_date, "%Y-%m-%d")[0:3]
        validity_date = datetime.datetime(y, m, d)
        identitycard.validity_date = validity_date

    identitycard.save()
    user.save()
    cache.delete('user_list')

    # 设计到更新数据库的操作一定要使用HttpResponseRedirect进行重定向跳转，以避免浏览器返回或重新发起请求
    # return HttpResponseRedirect(reverse('myapp:user_detail', args=(user.id,)))
    return redirect('myapp:user_detail', user_id=user.id)


def user_delete(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        raise Http404("user does not exist")  # 没有查询到数据则抛出404异常

    user.delete()
    cache.delete('user_list')

    return HttpResponseRedirect(reverse('myapp:user_index'))


def car_index(request):
    car_list = Car.objects.order_by('-id')[:10]
    context = {'car_list': car_list}
    return render(request, 'myapp/car/index.html', context)


def car_detail(request, car_id):
    if car_id == 0:
        car = None  # 此时就会给出新的ID,并发时不可以这样处理
    else:
        try:
            car = Car.objects.get(pk=car_id)
        except Car.DoesNotExist:
            raise Http404("Car does not exist")  # 没有查询到数据则抛出404异常
    users = User.objects.all()
    return render(request, 'myapp/car/detail.html', {'car': car, 'users': users, 'colors': utils.color})


def car_delete(request, car_id):
    try:
        car = Car.objects.get(pk=car_id)
    except Car.DoesNotExist:
        raise Http404("car does not exist")  # 没有查询到数据则抛出404异常

    car.delete()

    return HttpResponseRedirect(reverse('myapp:car_index'))


# 只允许接收post请求
@require_http_methods(["POST"])
# 关闭csrf验证
@csrf_exempt
def car_save(request):
    id = request.POST.get('id', None)  # id参数不存在时设置为None
    carNum = request.POST.get('carNum', None)
    carColor = request.POST.get('carColor', None)
    carPrice = request.POST.get('carPrice', None)
    users = request.POST.getlist('users', None)  # 获取list参数

    if id:
        car = Car.objects.get(pk=id)
    else:
        car = Car(carNum='', carColor=1, carPrice=0.00)

    if carColor:
        car.carColor = int(carColor)
    if carNum:
        car.carNum = carNum
    if carPrice:
        car.carPrice = carPrice

    # 在事务代码块中执行
    with transaction.atomic():
        if id and users:
            car.user.clear()  # 先清空在添加
            for userid in users:
                car.user.add(User.objects.get(pk=userid))

        car.save()

        with transaction.atomic(using='django2_db'):
            from django2.models.book import Book
            book = Book(bookname='mybook', bookpapers=100)
            book.save()
    return HttpResponseRedirect(reverse('myapp:car_detail', args=(car.id,)))


from django.core import serializers
from django.http import JsonResponse
from utils import JSONUtil


def user_query_json(request):
    user_list = User.objects.all()
    # user_list = serializers.serialize("json", user_list)
    # context = {'user_list': user_list}
    # return JsonResponse(context)
    # return JsonResponse(user_list, safe=False)  # safe=False可以传递对象，否则必须传递一个dict
    return JSONUtil.render_json(user_list, dict_key='user_list', safe=False)


def user_query_json_get(request, user_id):
    # 如果使用get方法活动对象，转换json时就要使用  user = JSONUtil.getJson(user)的方法，
    # 因为serialize只支持querySet对象
    user = User.objects.get(pk=user_id)
    # user = JSONUtil.getJson(user)
    # user = User.objects.filter(pk=user_id)
    from django.utils.translation import ugettext as _
    output = _('my test local')
    print(output)

    m = "may"
    d = "20"
    output = _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}
    print(output)

    # print('_language', request.session['_language'])

    return JSONUtil.render_json(user, dict_key='user', safe=False)
