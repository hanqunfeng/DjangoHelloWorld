# Django2学习笔记

## 摘要
版本：python3.6.4+django2.0.3

参考资料：

[官方资料](https://docs.djangoproject.com/en/2.0/)

[Django 1.8.2 文档](https://yiyibooks.cn/xx/django_182/index.html)

[Django 1.11.6 文档](https://yiyibooks.cn/xx/Django_1.11.6/index.html)

[Django 2.0.2文档](https://yiyibooks.cn/qy/django2/index.html)

[Django中文教程](https://code.ziqiangxuetang.com/django/django-internationalization.html)


## 1.安装
`pip install Django`
`python -m django --version`

## 2.创建新项目
`django-admin startproject mysite`  # mysite就是项目名称

## 3.创建新的应用
`python manage.py startapp polls` # polls是应用名称
settings.py中加入新应用配置
```python
INSTALLED_APPS = [
    'polls.apps.PollsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## 4.创建和更新数据库：
`python manage.py makemigrations` # 全部应用都会创建迁移文件
`python manage.py makemigrations polls` # 只创建指定的应用
`python manage.py migrate` # 执行迁移文件到数据库

查看迁移文件生成的sql:
 sqlmigrate命令接收迁移文件的名字并返回它们的SQL语句：#只是打印出要执行的sql语句

`python manage.py sqlmigrate polls 0001`  # 这里迁移文件的后缀_initial.py不需要。

## 5.启动服务器
Django的管理后台站点是默认启用的。 让我们启动开发服务器，然后探索它。
如果服务器没有运行，像下面这样启动它：

`python manage.py runserver`

现在，打开一个浏览器访问你本地域名中的 “/admin/” — 例如http://127.0.0.1:8000/admin/。

启动：

`python manage.py runserver 9000` #指定启动端口
`python manage.py runserver 0.0.0.0:9000` #指定启动ip+端口

## 6.测试：
`python manage.py test` #运行整个项目的全部tests.py

`python manage.py test django2` #运行指定模块的tests.py

`python manage.py test django2.tests.Django2Test` #测试指定模块的指定测试类

`python manage.py test django2.tests.Django2Test.test_sql` #测试指定模块的指定测试类指定方法

## 7.检查代码覆盖率：
`pip install coverage`
`coverage run my_program.py arg1 arg2`

django检查方法：

`coverage run --source='.' manage.py test myapp`

之后可以运行

`coverage report` ：显示结果

`coverage html`：生成html  测试会在当前项目下生成htmlcov目录，运行index.html即可查看

## 8.mysql:
`brew install mysql-connector-c`
`pip install mysqlclient`

需要提前创建好数据库
settings.py:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

数据库更新：
一般情况下，我们使用如下两个命令更新数据库

`python manage.py makemigrations` #生成数据库模型文件

`python manage.py migrate` #执行模型文件

或者：
`python  manage.py migrate --database=users` #指定数据库，默认为default

如果由于默写原因删除了数据库中对应的表，则再次执行上面的命令是不能重新创建成功的，原因是每次django执行模型文件时都会在django_migrations表中新增对应的log记录，删掉对应的log记录即可重新执行成功。

## 9.多数据源配置
django配置连接多个数据库，自定义表名称：
https://www.cnblogs.com/dreamer-fish/p/5469141.html

使用models文件夹维护model时，一定要在其下的__init__.py中添加对model的引用，
否则`python manage.py makemigrations` 命令不会创建出对应的迁移文件
比如：
```python
from .person import Person
from .user import User
from .identity_card import IdentityCard
from .car import Car
```
数据库路由:
settings.py:
```python
DATABASE_ROUTERS = ['django2.router.django2_router.Django2Router', ]
```

可以将对应的迁移文件的sql导入到指定的db，所以路由器的设置很重要
```python
def allow_migrate(self, db, app_label, model_name=None, **hints):
    if db == 'django2_db':  #如果指定了数据库
        return app_label == 'django2' #并且model被设置了正确的app_label，则可以执行迁移文件
    elif app_label == 'django2':
        return False
```
设置好数据库路由器后，执行python manage.py migrate --database=django2_db

## 10.缓存
说明：不推荐使用站点级缓存和页面级缓存，除非是展示信息类的网站，如果是频繁修改的站点，最好手工在代码中维护缓存。

1).memcached

`brew install memcached`

启动：`memcached -d -p 11211 -c 1024 -m 64`

-d:后台运行
-p:端口
-c:最大连接数
-m:最多分配内存


1.使用memcached：`pip install python-memcached`

2.settings

```python
# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600,  # 单位秒，默认300s, 60s * 10 = 10min
        'KEY_PREFIX': 'myapp',  # 缓存键的字符串前缀
    }
}
```

3.代码中
```python
from django.core.cache import caches
cache = caches['default']
```
```python
#如果希望使用默认的default，也可以
from django.core.cache import cache

cache.set('user_list', user_list)
user_list = cache.get('user_list')
user_list = cache.delete('user_list')
```

2).redis

参考资料：http://django-redis-chs.readthedocs.io/zh_CN/latest/

1.`brew install redis`

启动：`redis-server /usr/local/etc/redis.conf`

2.`pip install django-redis`

3.settings
```python
# 缓存设置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 600,  # 单位秒，默认300s, 60s * 10 = 10min
        'KEY_PREFIX': 'myapp',  # 缓存键的字符串前缀
    },
    "redis": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        'TIMEOUT': 600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds socket 建立连接超时设置
            "SOCKET_TIMEOUT": 5,  # in seconds 连接建立后的读写操作超时设置
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",  # 压缩支持
            "IGNORE_EXCEPTIONS": True,  # 如果redis服务关闭，不会引起异常，memcached默认支持
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}  # 连接池
        }
    }
}
# redis记录异常日志
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = True
```
4.代码中
```python
from django.core.cache import caches
redis_cache = caches['redis']

redis_cache.set('user_list', user_list)
user_list = redis_cache.get('user_list')
user_list = redis_cache.delete('user_list')
```

## 11.注册模板自定义方法:
1.创建myapp.libraries.utils.py
```python
from django import template
register = template.Library()
color = ((1, 'red'), (2, 'black'), (3, 'blue'))

# @register.filter使用方法，最多两个参数
# {{ car.carColor|getcolorstr }}
# {{ car.carColor|getcolorstr:param2 }} 前面的表示第一个参数
@register.filter
def getcolorstr(colorNum):
    return color[colorNum - 1][1]


# @register.simple_tag使用方法，不限制参数个数
# {% getcolorstr2 car.carColor %}
# {% getcolorstr2 param1 param2 param3 %}
@register.simple_tag
def getcolorstr2(colorNum):
    return color[colorNum - 1][1]
```

2.settings:在模板配置中加入libraries配置
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'utils': 'myapp.libraries.utils',
            },
        },
    },
]
```
3.模板页面中使用
```html
{% load utils %}
{{ car.carColor|getcolorstr }}
{% getcolorstr2 car.carColor %}
```

## 12.模板
1.转义:
由于模板系统没有“转义”的概念，为了显示模板标签中使用的一个位，必须使用{％ templatetag ％}标记。
```
论据 输出
openblock {％
closeblock ％}
openvariable {{
closevariable }}
openbrace {
closebrace }
opencomment {＃
closecomment ＃}
```
例如：
```
{% templatetag openblock %} url 'entry_list' {% templatetag closeblock %}
```
或者使用如下方式：被包含的内容不会被模板引擎转意，将直接输出
```
{% verbatim myblock %}
    Avoid template rendering via the {% verbatim %}{% endverbatim %} block.
{% endverbatim myblock %}
```
2.for:
```
变量 描述
forloop.counter 循环的当前迭代（1索引）
forloop.counter0 循环的当前迭代（0索引）
forloop.revcounter 循环结束的迭代次数（1索引）
forloop.revcounter0 循环结束的迭代次数（0索引）
forloop.first 如果这是第一次通过循环，则为真
forloop.last 如果这是最后一次循环，则为真
forloop.parentloop 对于嵌套循环，这是围绕当前循环的循环
```

## 13.自定义400、403、404、500页面
1.settings.py中DEBUG = False，否则自定义页面不起作用

2.在任意模块下的views.py中增加如下方法，也可以在主模块中创建一个views.py
方法处理逻辑可以参考：~venv/lib/python3.6/site-packages/django/views/defaults.py中对各个方法的定义
```python
from django.shortcuts import render

def bad_request(request, exception, template_name='400.html'):
    return render(request, template_name)


def permission_denied(request, exception, template_name='403.html'):
    return render(request, template_name)


def page_not_found(request, exception, template_name='404.html'):
    context = {'exception': exception}
    return render(request, template_name, context=context)


def server_error(request, template_name='500.html'):
    return render(request, template_name)
```

3.在项目根目录下的templates下创建对应的400.html、403.html、404.html、500.html，内容更加需要自定义，也可以参考~venv/lib/python3.6/site-packages/django/views/templates下的对应文件

4.在主模块下urls.py中增加如下配置:
```python
handler400 = 'DjangoHelloWorld.views.bad_request' #模块名称.views.方法名称
handler403 = 'DjangoHelloWorld.views.permission_denied'
handler404 = 'DjangoHelloWorld.views.page_not_found'
handler500 = 'DjangoHelloWorld.views.server_error'
```

## 14.Django配置session超时
#配置失效时间为半个小时
SESSION_COOKIE_AGE = 60*30
#关闭浏览器清除cookie
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

## 15.json与xml
1.json
创建一个JSONUtil工具类，用于返回json数据
```python
import json
from django.core.serializers import serialize, deserialize
from django.db import models
from django.db.models.query import QuerySet
from django.http import JsonResponse

# 反序列化
def json_to_list(json):
    if json[0] == '[':
        deserializedObjectList = deserialize('json', json)
    else:
        deserializedObjectList = deserialize('json', '[' + json + ']')
    list = []
    for deserializedObject in deserializedObjectList:
        list.append(deserializedObject.object)
    return list


# 序列化
def to_json(obj):
    if isinstance(obj, models.Model):
        obj = [obj]  # 因为serialize只支持可迭代对象，比如querySet对象
    data = serialize("json", obj)
    return data


# 该方法没有做严格的验证，只支持dict,models.Model,models.QuerySet，可以根据需要自行扩展
def render_json(data, dict_key='data', **response_kwargs):
    if isinstance(data, dict):
        return JsonResponse(data)
    data = to_json(data)
    if 'safe' in response_kwargs and response_kwargs['safe'] is False:
        pass
    else:
        data = {dict_key: data}  # 默认必须传递字典数据
    if isinstance(data, str):  # 由于非字典类型的数据会被当做字符串处理，即返回结果两边都有引号，所以此处将其转换为对象，否则ajax调用时不方便处理
        data = json.loads(data)
    return JsonResponse(data, **response_kwargs)
```

view.py中：
```python
def user_query_json(request):
    user_list = User.objects.all()
    return JSONUtil.render_json(user_list, safe=False) # safe=False可以传递对象，否则必须传递一个dict，ajax请求时这样要设置safe=False，这样页面可以直接获取到对象
```
返回结果，可以看到两边没有引号：
[{"model": "myapp.user", "pk": 4, "fields": {"name": "\u54c8\u54c8", "birth_day": "2018-04-09", "phone": "None", "email": "None"}}, {"model": "myapp.user", "pk": 9, "fields": {"name": "\u5929\u738b\u5c71", "birth_day": "2018-09-10", "phone": "123", "email": "123@123.com"}}]

```python
def user_query_json_get(request, user_id):
    user = User.objects.get(pk=user_id)
    # user = User.objects.filter(pk=user_id)
    return JSONUtil.render_json(user, dict_key='user', safe=True)
```
返回结果：[{"model": "myapp.user", "pk": 1, "fields": {"name": "\u97e9\u7fa4\u5cf0", "birth_day": "2018-04-07", "phone": "None", "email": "qunfeng_han@126.com"}}]

模板中：
```html
<script src="{% static 'polls/js/jquery-1.11.0.min.js' %}"></script> #注意这里必须有闭合标签</script>，否则显示会有问题

<div id="userdiv"></div>
<div id="userlistdiv"></div>

<script>

    $.getJSON("{% url 'myapp:user_query_json_get' 1 %}", function(ret) {
        $.each(ret, function (key, value) {
            // key 为字典的 key，value 为对应的值
            $("#userdiv").append(value.pk+"#"+value.fields.name+"#"+value.fields.birth_day+"#"+value.fields.phone+"#"+value.fields.email+"<br>")

        });
    });

    $.getJSON("{% url 'myapp:user_query_json' %}", function(ret) {
        $.each(ret, function (key, value) {
            // key 为字典的 key，value 为对应的值
            $("#userlistdiv").append(value.pk+"#"+value.fields.name+"#"+value.fields.birth_day+"#"+value.fields.phone+"#"+value.fields.email+"<br>")

        });
    })

</script>
```

2.xml

XMLUtil.py

```python
# -*- coding=utf-8 -*-
from django.core import serializers
from django.db import models
from django.db.models.query import QuerySet
from django.http import HttpResponse


def render_xml(data):
    data = to_xml(data)
    response = HttpResponse(data)
    response['Content-Type'] = 'application/xml'
    return response

# 序列化
def to_xml(data):
    if isinstance(data, models.Model):
        data = [data]  # 因为serialize只支持可迭代对象，比如querySet对象
    elif isinstance(data, QuerySet):
        data = data
    else:
        pass
    data = serializers.serialize("xml", data)
    return data

# 反序列化
def xml_to_list(xml):
    deserializedObjectList = serializers.deserialize("xml", xml)
    list = []
    for deserializedObject in deserializedObjectList:
        list.append(deserializedObject.object)
    return list
```
views.py
```python
from utils import XMLUtil

def user_query_xml(request):
    user_list = User.objects.all()
    return XMLUtil.render_xml(user_list)

def user_query_xml_get(request, user_id):
    user = User.objects.get(pk=user_id)
    return XMLUtil.render_xml(user)
```
输出结果
```xml
<?xml version="1.0" encoding="utf-8"?>
<django-objects version="1.0">
    <object model="myapp.user" pk="4">
        <field name="name" type="CharField">哈哈</field>
        <field name="birth_day" type="DateField">2018-04-09</field>
        <field name="phone" type="CharField">13800138000</field>
        <field name="email" type="CharField">138@qq.com</field>
    </object>
    <object model="myapp.user" pk="2">
        <field name="name" type="CharField">张三</field>
        <field name="birth_day" type="DateField">
            <None></None>
        </field>
        <field name="phone" type="CharField">
            <None></None>
        </field>
        <field name="email" type="CharField">zhansan@163.com</field>
    </object>
</django-objects>
```



js:
```javascript
$.ajax({
    url:"{% url 'myapp:user_query_xml' %}",
    type:"GET",
    dataType:'xml',
    success:function(xml){
        $(xml).find("object").each(function(i) {
            //获取id
            var id=$(this).attr("pk");
            var content = "";
            $(this).find("field").each(function(j){
                content += $(this).attr('name') + "==" + $(this).text() + "#"
            })
            $("#userdivxml").append(id+ "#" + content +"<br>")

        });
    },
    error:function(){ alert("加载失败"); }
})
```

## 16.response添加相应头
一般我们返回视图时都是调用
from django.shortcuts import render的render(request, 'myapp/user/index.html', context)
实际上它返回的是一个HttpResponse对象，我们可以这样为其添加返回头
```python
response = render(request, 'myapp/user/index.html', context)
response['Last-Modified'] = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
return response
```


## 17.多语言
参考：https://code.ziqiangxuetang.com/django/django-internationalization.html

1.`brew install gettext`

2.pip的bug，需要手工处理
/venv/lib/python3.6/site-packages/pip-9.0.1-py3.6.egg/pip/_vendor/webencodings/
修改3个文件：
__init__.py，
tests.py，
x_user_defined.py，
将：utf8 修改为 utf-8.
3.settings.py
```python
LANGUAGE_CODE = 'zh-hans'  # 英文是en，这里是中文，注意这里必须配置为zh-hans，而下面创建和编译语言文件是要使用zh_hans
USE_I18N = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'myapp/locale'), # 应用下的路径
    os.path.join(BASE_DIR, 'locale'),
)
```
注意：这里『locale』文件夹需要手工创建，默认就是项目根路径下的locale目录。
这里需要注意一点，如果应用下面创建了locale并且配置到LOCALE_PATHS中，则后面执行创建命令时，无论是在项目根路径下执行还是在应用下执行，都只会将语言文件创建到应用下的locale中。如果应用下没用locale目录则需要在项目根路径下执行命令，并且创建到项目根路径下的locale目录中。

4.在代码中加入一些多语言对应的内容
代码中
```python
from django.utils.translation import ugettext as _
 output = _('Today is %(month)s %(day)s.') % {'month': m, 'day': d}
```
模板页面中可以直接使用下划线的别名形式
```html
{{ _('Django site admin') }}<br>
{{ _('my test local') }}<br>
```

这里注意，如果要使用『trans』标签，必须在页面中加载{% load i18n %}
```html
{% load i18n %}
{% trans "my test local" %}<br>

{#将翻译结果保存到变量中#}
{% trans "my test local" as mylocal %}
{{ mylocal }}<br>

{#设置局部显示的语言，下面的内容将显示对应的英文内容，但只在区块内有效#}
{% language 'en' %}
    {% get_current_language as LANGUAGE_CODE %}
    Current language: {{ LANGUAGE_CODE }} <br>  #区块内显示en
    {{ _('Django site admin') }}<br>
{% endlanguage %}

{% get_current_language as LANGUAGE_CODE %}
    Current language: {{ LANGUAGE_CODE }} <br>  #区块外显示zh-hans
```
如果没有找到对应的key值，则会直接显示待翻译的key值字符串；
如果对应的语言包下没有找到key值，而默认语言包下有对应的key值，则会显示默认的语言，如LANGUAGE_CODE = 'zh-hans'

PS:如果需要翻译的内容包含变量，比如_('Today is %(month)s %(day)s.') ，最好在后台处理好后做为变量传递到模板页面上，目前暂不知道如何在模板中直接处理。


5.创建或更新语言文件

`django-admin makemessages -l en` # 英文

`django-admin makemessages -l zh_hans` #指定中文语言，注意这里不要写成zh-hans

会在locale目录下生成对应的语言包django.po

`django-admin makemessages -a` #全部语言

说明：如果在项目根路径下执行，会将项目中所有应用都扫描一遍并汇总合并到一起，如果在某个应用下执行命令，则只会扫描当前应用，并在其下的locale目录下创建文件，优先级根据settings中配置的LOCALE_PATHS的顺序而定。

6.编译

`django-admin compilemessages --locale zh_hans` #指定语言

`django-admin compilemessages` # 全部语言
* django.po---->diango.mo

7.语言切换

1）在settings中的中间件配置中加入如下配置：
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
2）url中加入配置：
```python
path('i18n/', include('django.conf.urls.i18n')), #对应下面的{% url 'set_language' %}
```
变更后的语言会保存在session中，可以通过`request.session['_language']`获得

3）在模板页面中需要切换语言的地方加入如下代码：
```html
<form action="{% url 'set_language' %}" method="post">{% csrf_token %}
    <input name="next" type="hidden" value="{{ redirect_to }}" />
    <select name="language">
        {% get_current_language as LANGUAGE_CODE %}
        {% get_available_languages as LANGUAGES %}
        {% get_language_info_list for LANGUAGES as languages %}
        {% for language in languages %}
            <option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}>
                {{ language.name_local }} ({{ language.code }})
            </option>
        {% endfor %}
    </select>
    <input type="submit" value="Go" />
</form>
```

说明：
redirect_to：如果不设置就会返回当前页面，设置的话就会跳转到设置的页面
这里get_available_languages会显示所有支持的语言，不过一般项目不会支持这么多的语言，所以可以在settings中增加配置来明确语言范围：
```python
LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)
```

4）js中使用多语言
js需要单独处理，比如我们写了一个js文件，路径为project/myapp/static/myapp/js/test.js
```javascript
a = gettext('wwww hhhh')
alert(a)
```
模板中引入：
#下面这个是动态js，必须引入，否则gettext方法不起作用
```html
<script type="text/javascript" src="{% url 'javascript-catalog' %}"></script>
<script src="{% static 'myapp/js/test.js' %}"></script>
```

urls加入对javascript-catalog的支持：
`path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),``

执行如下命令：

`django-admin makemessages -d djangojs  -l zh_hans`
此时会在应用下的locale中生成djangojs.po文件（如果配置了应用locale，否则会在项目下的locale中创建）

`django-admin compilemessages --locale zh_hans`
此时会将djangojs.po编译为djangojs.mo

如果直接将带翻译的js代码写在模板页面中，暂时不清楚要通过什么命令实现，不过可以有个折中的办法，就是创建一个js文件，然后将所有需要翻译的内容都加上，然后运行上面两个命令，这样django在运行模板中的js时同样可以完成翻译
模板中：
```javascript
<script>
    alert(gettext('hello js'))
    alert(gettext('o my god'))
</script>
```
js中：只要js代码中出现翻译方法的地方都会被加入翻译，这个js不需要被任何模板引入，也不需要被同步到静态文件夹中，仅仅是为生成翻译文件而存在
```javascript
gettext('hello js')
gettext('o my god')
```


## 18.日志
1.settings
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用logger，建议设置为False
    'formatters': {  # 日志格式，提供给handler使用，非必须，如果不设置格式，默认只会打印消息体
        'verbose': {  # 格式名称
            # INFO 2018-04-25 15:43:27,586 views 8756 123145350217728 这是一个日志
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            # INFO  这是一个日志
            'format': '%(levelname)s %(message)s'
        },
        'standard': {
            # 2018-04-25 16:40:00,195 [Thread-7:123145575223296] [myapp.log:282] [views:user_query_json_get] [INFO]- 这是一个日志
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'
        },

    },
    'filters': {  # 过滤器，提供给handler使用，非必须
        'require_debug_true': {  # 要求DEBUG=True时才打印日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 处理器，设置日志记录方式，必须
        'console': {  # 处理器名称
            'level': 'DEBUG',  # 设置级别
            'filters': ['require_debug_true'],  # 设置过滤器，多个用逗号分割
            'class': 'logging.StreamHandler',  # 处理器，这里是控制台打印
            'formatter': 'verbose'  # 设置日志格式
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  # 记录到文件
            'filename': '/Users/hanqunfeng/python_workspace/log/file.log',
            'formatter': 'verbose'
        },
        'rotatingFile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',  # 按文件大小切割日志
            # 'filename': 'log/all.log',  # 日志输出文件 默认在当前项目根路径下
            'filename': '/Users/hanqunfeng/python_workspace/log/rotatingFile.log',  # 日志输出文件
            'maxBytes': 1024 * 1024 * 5,  # 每个文件大小
            'backupCount': 5,  # 保留日志份数，只保留最后5份，如果都保留，设置为0，默认就是0
            'formatter': 'standard',  # 使用哪种formatters日志格式
        },
		'timedRotatingFile': {
		    'level': 'DEBUG',
		    'class': 'logging.handlers.TimedRotatingFileHandler',  # 按时间切割日志
		    'filename': '/Users/hanqunfeng/python_workspace/log/timedRotatingFile.log',  # 日志输出文件
		    'when': 'D',  # 按天分割
		    'backupCount': 5,  # 保留日志份数，只保留最后5份，如果都保留，设置为0，默认就是0
		    'formatter': 'standard',  # 使用哪种formatters日志格式
		},
    },
    'loggers': {#日志记录器
        'django': {#日志名称路径前缀，即logging.getLogger(__name__)获取logger对象时，_name__得到的前缀与之匹配即可，比如__name__得到的是django.server
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),  # 只有设置DEBUG = True时，该配置才会打印sql信息
        },
        'django.request': {
            'handlers': ['rotatingFile'],
            'level': 'ERROR',
            'propagate': False,  # 设置为False，表示不像其父级别传递日志内容
        },
        'myapp.log': { # 也可以这样创建logger对象，logging.getLogger('myapp.log')
            'handlers': ['file', 'timedRotatingFile'],
            'level': 'INFO',  # 这里的日志级别不能低于处理器中设置的日志级别
        },
    },
}
```

代码中使用方式：
```python
# 导入logging库
import logging
# 获取logger的一个实例
# logger = logging.getLogger(__name__)
logger = logging.getLogger('myapp.log')

# 方法中：
logger.info('这是一个日志')
```

## 19.发送邮件
1.settings
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xxx@163.com'  # 帐号
EMAIL_HOST_PASSWORD = 'xxxxxxx'  # 密码
DEFAULT_FROM_EMAIL = 'hanqf <xxx@163.com>'
```
2.代码里
```python
from django.conf import settings
# 发送邮件
from django.core.mail import send_mail
send_mail('Subject here主题', 'Here is the message.消息', settings.DEFAULT_FROM_EMAIL,
          ['qunfeng_han@126.com'], fail_silently=False)

# 一次可以发送多组邮件
from django.core.mail import send_mass_mail

message1 = ('Subject here', 'Here is the message', settings.DEFAULT_FROM_EMAIL,
            ['qunfeng_han@126.com', 'hanqunfeng@lkmotion.com'])
message2 = ('Another Subject', 'Here is another message', settings.DEFAULT_FROM_EMAIL, ['qunfeng_han@126.com'])
send_mass_mail((message1, message2), fail_silently=False)

# 可以这是抄送附件等
from django.core.mail import EmailMultiAlternatives
msg = EmailMultiAlternatives('主题', '内容', settings.DEFAULT_FROM_EMAIL, ['qunfeng_han@126.com'],
                             cc=['hanqunfeng@lkmotion.com'])
# msg.content_subtype = "html" # 设置邮件格式，html可以发送内容为html，不推荐这么使用，可以使用下面的方式
html_content = '<p>这是一封<strong>重要的</strong>邮件.</p>'
msg.attach_alternative(html_content, "text/html")  # 如果接收方的邮件支持html，则显示该信息，否则显示原「内容」
# 添加附件（可选）
msg.attach_file('/Users/hanqunfeng/python_workspace/STATIC_ROOT/polls/images/background.jpg')
# 发送
msg.send()

```

## 20.main方法测试
mian方法测试一定要在如下情况下使用，这样可以保证当前模块被别处引用时不会触发如下测试代码，只有独立运行该模块时才会执行。
```python
if __name__ == '__main__':
    # 加载环境配置
    import django, os
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoHelloWorld.settings")
    django.setup()
    # 以下是测试内容
    from myapp.models.user import User
    user_list = User.objects.all()
    xml = to_xml(user_list)
    print(xml)
```

## 21.Signal，信号，有点类似MQ
1.定义信号和接收器
```python
from django.dispatch import Signal, receiver
# my_singal = Signal()
my_singal = Signal(providing_args=["key1", "key2"]) # 定义信号接收的参数，不指定参数也可以

@receiver(my_singal)
def my_callback(sender, **kwargs): # 接收器回调函数
    print(sender)
    print(kwargs)
    for key in kwargs:
        print(key)
        print(kwargs[key])
    print("Request finished!")
```
2.发送信号，发送信号时接收器就会被执行
```python
from signals.signals import my_singal
my_singal.send(sender=__name__, key1='qqq', key2=10, key3=100) # 实际上可以多发送一些参数
```


## 22.Django管理后台简介
首先，我们需要创建一个能够登录管理后台站点的用户。
运行如下命令：
```
python manage.py createsuperuser
```

键入你想要使用的用户名，然后按下回车键：
```
Username: admin
```

然后提示你输入想要使用的邮件地址：
```
Email address: admin@example.com
```

你需要输入两次密码，第二次输入是确认密码
```
Password: **********
Password (again): *********
Superuser created successfully.
```

PS：管理员密码忘记了可以通过如下方法修改：
```shell
$ python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(pk=1) # 可以通过查询获得用户对象
>>> user.set_password('hqf25485090')
>>> user.save()
>>> quit()
```




## 23.部署正式环境
settings.py:
```python
DEBUG = False # 此时很多问题就会出现，需要增加很多额外的配置才能正常工作，这也是为了包含生产环境吧

ALLOWED_HOSTS = ['127.0.0.1']

STATIC_URL = 'http://localhost/static/'      # apache部署的静态文件服务器访问地址

STATIC_ROOT = "/Users/hanqunfeng/python_workspace/STATIC_ROOT/"  #apache 服务目录

# 上传文件路径
MEDIA_URL = 'http://localhost/media/'
MEDIA_ROOT = '/Users/hanqunfeng/python_workspace/MEDIA/'
```

apache配置：
```shell
Alias /media/ /Users/hanqunfeng/python_workspace/MEDIA/
Alias /static/ /Users/hanqunfeng/python_workspace/STATIC_ROOT/

<Directory /Users/hanqunfeng/python_workspace/STATIC_ROOT>
Require all granted
</Directory>

<Directory /Users/hanqunfeng/python_workspace/MEDIA/>
Require all granted
</Directory>
```
使用如下命令可以将本地的静态资源部署到apache服务目录：
```shell
python manage.py collectstatic
```

模板页面：
```html
{% load static %}

<link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}" />
```

上传文件：
model中：
```python
photo = models.ImageField(upload_to="photo", default="default/django.jpeg")  # 路径相对于MEDIA_ROOT的配置
```
之后要注意更新数据库。

需要安装Pillow，否则会报错
```
ERRORS:
polls.Question.photo: (fields.E210) Cannot use ImageField because Pillow is not installed.
	HINT: Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".
```
```
pip install Pillow
```

如果要在页面中使用settings中的变量，需要在当前应用中创建一个context_processors.py 文件
```python
from django.conf import settings  # import the settings file

def settings_constant(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'MEDIA_URL': settings.MEDIA_URL, 'DEBUG': settings.DEBUG}
```
并在settings文件配置如下

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'polls.context_processors.settings_constant', #应用名称.文件名称.方法名称
            ],
        },
    },
]
```
模板页面中：
```html
<form enctype="multipart/form-data">
<img src="{{MEDIA_URL}}abc/a.png">
<input type="file" name="photo" id="id_photo" />
</form>

也可以使用下面的形式获得上传文件的url，
即使用上传文件字段的url属性：{{ question.photo.url }}
<a href="{{MEDIA_URL}}{{ question.photo }}">{{ question.photo }}</a> ##
<a href="{{ question.photo.url }}">{{ question.photo }}</a>
```

views处理代码中：
```python
input_img = request.FILES['photo']
question.photo = input_img
question.save()
```


部署到apache：

下载mod_wsgi：https://github.com/GrahamDumpleton/mod_wsgi/releases
```
tar xvfz mod_wsgi-X.Y.tar.gz
./configure --with-apxs=/Applications/XAMPP/bin/apxs --with-python=/Library/Frameworks/Python.framework/Versions/3.6/bin/python3

make
make install
```

然后在apache配置文件中加入如下配置
```
LoadModule wsgi_module modules/mod_wsgi.so
```
普通模式：
```
WSGIPythonHome /Users/hanqunfeng/python_workspace/DjangoHelloWorld/venv
WSGIPythonPath /Users/hanqunfeng/python_workspace/DjangoHelloWorld
```
或者采用守护进程模式：
```
WSGIDaemonProcess example.com python-home=/Users/hanqunfeng/python_workspace/DjangoHelloWorld/venv python-path=/Users/hanqunfeng/python_workspace/DjangoHelloWorld

WSGIProcessGroup example.com
```
配置项目访问路径
```
WSGIScriptAlias /mysite /Users/hanqunfeng/python_workspace/DjangoHelloWorld/DjangoHelloWorld/wsgi.py

<Directory /Users/hanqunfeng/python_workspace/DjangoHelloWorld/DjangoHelloWorld>
<Files wsgi.py>
Require all granted
</Files>
</Directory>
```
访问地址：http://127.0.0.1/mysite/polls
