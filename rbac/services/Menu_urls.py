#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django.urls import reverse
from django.http import QueryDict


def memory_cul(request, name, *args, **kwargs):

    '''
    生成带有搜索条件的URL(替代了模板中的URL)
    :param request:
    :param name:
    :return:
    '''

    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 当前URL中无参数
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()
    # query_dict.urlencode() # filter=mid=26&age=99

    return "%s?%s" % (basic_url, query_dict.urlencode())


def memory_resverse(request, name, *args, **kwargs):

    '''
    反向生成URL
        http://127.0.0.1:8000/rbac/menu/add/?_filter=mid%3D1
       1、 把原来获取到原来搜索条件 如： _filter
       2、 reverse生成原来的URL，如、/menu/list/
       3、 /menu/list/?mid%3D1 拼接
    :param request:
    :param name:
    :param args:
    :param kwargs:
    :return:
    '''

    url = reverse(name, args=args, kwargs=kwargs)
    origin_params = request.GET.get("_filter")
    if origin_params:
        url = "%s?%s" % (url, origin_params)
    return url
