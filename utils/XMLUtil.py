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
        data = [data]  # 因为serialize只支持querySet对象
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


if __name__ == '__main__':
    import django, os

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "DjangoHelloWorld.settings")

    django.setup()
    from myapp.models.user import User

    user_list = User.objects.all()
    xml = to_xml(user_list)
    print(xml)
