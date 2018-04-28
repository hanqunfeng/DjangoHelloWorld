# -*- coding=utf-8 -*-

import json

from django.core.serializers import serialize, deserialize
from django.db import models
from django.db.models.query import QuerySet
from django.http import JsonResponse


class MyEncoder(json.JSONEncoder):
    """ 继承自simplejson的编码基类，用于处理复杂类型的编码
    """

    def default(self, obj):
        if isinstance(obj, QuerySet):
            """ Queryset实例
            直接使用Django内置的序列化工具进行序列化
            但是如果直接返回serialize('json',obj)
            则在json序列化时会被从当成字符串处理
            则会多出前后的双引号
            因此这里先获得序列化后的对象
            然后再用json反序列化一次
            得到一个标准的字典（dict）对象
            """
            return json.loads(serialize('json', obj))
        if isinstance(obj, models.Model):
            """
            如果传入的是单个对象，区别于QuerySet的就是
            Django不支持序列化单个对象
            因此，首先用单个对象来构造一个只有一个对象的数组
            这是就可以看做是QuerySet对象
            然后此时再用Django来进行序列化
            就如同处理QuerySet一样
            但是由于序列化QuerySet会被'[]'所包围
            因此使用string[1:-1]来去除
            由于序列化QuerySet而带入的'[]'
            """
            return json.loads(serialize('json', [obj])[1:-1])
        if hasattr(obj, 'isoformat'):
            # 处理日期类型
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


def to_json2(obj):
    """    使用MyEncoder这个自定义的规则类来序列化对象
    """
    # result = dict(args)
    return json.dumps(obj, cls=MyEncoder)


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


if __name__ == '__main__':
    pass
