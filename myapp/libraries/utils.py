from django import template

register = template.Library()

color = ((1, 'red'), (2, 'black'), (3, 'blue'))


# 使用方法：
# 1.在settings中注册该libraries
# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')]
#         ,
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': [
#                 'django.template.context_processors.debug',
#                 'django.template.context_processors.request',
#                 'django.contrib.auth.context_processors.auth',
#                 'django.contrib.messages.context_processors.messages',
#                 'polls.context_processors.settings_constant',
#             ],
#             'libraries': {  # Adding this section should work around the issue.
#                 'utils': 'myapp.libraries.utils',
#             },
#         },
#     },
# ]


# 2.在模板页面中引用该libraries
# {% load utils %}


# 3.@register.filter使用方法，最多两个参数
# {{ car.carColor|getcolorstr }}
# {{ car.carColor|getcolorstr:param2 }} 前面的表示第一个参数

@register.filter
def getcolorstr(colorNum):
    return color[colorNum - 1][1]


# 4.@register.simple_tag使用方法，不限制参数个数
# {% getcolorstr2 car.carColor %}
# {% getcolorstr2 param1 param2 param3 %}
@register.simple_tag
def getcolorstr2(colorNum):
    return color[colorNum - 1][1]
