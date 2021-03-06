"""
Django settings for DjangoHelloWorld project.

Generated by 'django-admin startproject' using Django 2.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# 项目根路径 /Users/hanqunfeng/python_workspace/DjangoHelloWorld
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c38#=^58f6(5wjo&0xbeg9n-h9w)x1!(%!j_4a2=9zwp1c=$jn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False  # 此时很多问题就会出现，需要增加很多额外的配置才能正常工作，这也是为了包含生产环境吧

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
            'formatter': 'standard'  # 设置日志格式
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
    'loggers': {  # 日志记录器
        'django': {  # 日志名称路径前缀，即logging.getLogger(__name__)获取logger对象时，_name__得到的前缀与之匹配即可，比如__name__得到的是django.server
            'handlers': ['console'],
            'propagate': True,
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),  # 只有设置DEBUG = True时，该配置才会打印sql信息
        },
        'django.request': {
            'handlers': ['rotatingFile'],
            'level': 'ERROR',
            'propagate': True,  # 设置为False，表示不像其父级别传递日志内容
        },
        'django.db': {  # sql打印
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # 设置为False，表示不像其父级别传递日志内容
        },
        'django_redis': {  # redis
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,  # 设置为False，表示不像其父级别传递日志内容
        },
        'myapp': {  # 也可以这样创建logger对象，logging.getLogger('myapp.log')
            'handlers': ['console', 'file', 'rotatingFile', 'timedRotatingFile'],
            'level': 'INFO',  # 这里的日志级别不能低于处理器中设置的日志级别
        },
    },
}

# ALLOWED_HOSTS = ['127.0.0.1']
ALLOWED_HOSTS = ['*', ]  # 允许所有机器访问

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'polls.apps.PollsConfig',
    'myapp.apps.MyappConfig',
    'django2.apps.Django2Config',
    'django3.apps.Django3Config',
]

MIDDLEWARE = [
    # UpdateCacheMiddleware
    # 在每个HttpResponse里自动设置了一些头部信息
    # 设置 Expires 头 为当前日期/时间加上定义的CACHE_MIDDLEWARE_SECONDS.
    # 设置 Cache-Control头部来给页面一个最长的有效期, 来自 CACHE_MIDDLEWARE_SECONDS 的设置.
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # FetchFromCacheMiddleware
    # 缓存GET和HEAD状态为200的回应， 用不同的参数请求相同的url被视为独立的页面，缓存是分开的
    # 'django.middleware.cache.FetchFromCacheMiddleware',
]
# 不要使用站点级别缓存配置，除非网站只作为查询使用，如果频繁修改或者涉及到前端用户修改已经缓存的数据会导致页面内容无法更新
# CACHE_MIDDLEWARE_ALIAS = 'default'  # 用于存储的缓存的别名
# CACHE_MIDDLEWARE_SECONDS = 600  # 每个page需要被缓存多少秒
# CACHE_MIDDLEWARE_KEY_PREFIX = 'myappc'  # key前缀

# 根URLconf 模块，所有请求都从这个配置指定的文件中查找
ROOT_URLCONF = 'DjangoHelloWorld.urls'

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
                # 'django.template.context_processors.i18n',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'polls.context_processors.settings_constant',
            ],
            'libraries': {  # Adding this section should work around the issue.
                'utils': 'myapp.libraries.utils',
            },
        },
    },
]

WSGI_APPLICATION = 'DjangoHelloWorld.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django',
        'USER': 'django',
        'PASSWORD': 'django',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
        # 'ATOMIC_REQUESTS': True,  # 每个请求用事务包装起来，这样会带来性能影响，因为请求相应过程中会有一些非数据库的代码，会占用执行时间
    },

    'django2_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django2',
        'USER': 'django2',
        'PASSWORD': 'django2',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
        # 'ATOMIC_REQUESTS': True,  # 每个请求用事务包装起来，这样会带来性能影响，因为请求相应过程中会有一些非数据库的代码，会占用执行时间
    },

    'django3_db': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django3',
        'USER': 'django3',
        'PASSWORD': 'django3',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'STRICT_TRANS_TABLES',
        },
        # 'ATOMIC_REQUESTS': True,  # 每个请求用事务包装起来，这样会带来性能影响，因为请求相应过程中会有一些非数据库的代码，会占用执行时间
    }
}

# 数据库路由
DATABASE_ROUTERS = ['django2.router.django2_router.Django2Router', 'django3.router.django3_router.Django3Router']

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'  # 中文
# LANGUAGE_CODE = 'en'  # 英文

# TIME_ZONE = 'UTC'  # Asia/Shanghai
TIME_ZONE = 'Asia/Shanghai'  # Asia/Shanghai  中国时区

USE_I18N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'myapp/locale'),
    os.path.join(BASE_DIR, 'locale'),
)
LANGUAGES = (
    ('en', ('English')),
    ('zh-hans', ('中文简体')),
    ('zh-hant', ('中文繁體')),
)
USE_L10N = True

USE_TZ = True

# 默认值：'utf-8'.用于解码从磁盘读取的任何文件的字符编码。 这包括模板文件和初始SQL数据文件。
FILE_CHARSET = 'utf-8'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = '/static/'
STATIC_URL = 'http://localhost/static/'

STATIC_ROOT = '/Users/hanqunfeng/python_workspace/STATIC_ROOT/'

# 上传文件路径
MEDIA_URL = 'http://localhost/media/'
MEDIA_ROOT = '/Users/hanqunfeng/python_workspace/MEDIA/'

# MEDIA_ROOT = os.path.join(BASE_DIR, 'media/img')


# 配置失效时间为半个小时
SESSION_COOKIE_AGE = 60 * 30
# 关闭浏览器清除cookie
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

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
# DJANGO_REDIS_LOGGER = 'some.specified.logger'

# email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'xxxxx@163.com'  # 帐号
EMAIL_HOST_PASSWORD = 'xxxxxxxxx'  # 密码
DEFAULT_FROM_EMAIL = 'hanqf <xxxxx@163.com>'
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# 密码哈希算法，默认使用第一个加密，后面的可以用于老密码的验证，但是验证成功后会自动转换为第一种加密算法
# argon2的算法要优于md5
# 'django.contrib.auth.hashers.MD5PasswordHasher'
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]
