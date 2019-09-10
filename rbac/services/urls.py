#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django.urls import reverse
from django.http import QueryDict


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name:
    :return:
    """
    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 当前URL中无参数
    if not request.GET:
        return basic_url

    query_dict = QueryDict(mutable=True)
    query_dict['_filter'] = request.GET.urlencode()  # mid=2&age=99

    return "%s?%s" % (basic_url, query_dict.urlencode())