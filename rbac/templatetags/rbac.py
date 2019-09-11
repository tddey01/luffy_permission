#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-


import re
from django.template import Library
from django.conf import settings
from collections import OrderedDict
# from django.urls import reverse
# from django.http import QueryDict
from rbac.services import Menu_urls

register = Library()


@register.inclusion_tag('rbac/static_menu.html')
def static_menu(request):
    '''
    创建一级菜单
    :return:
    '''
    menu_list = request.session[settings.MENU_SISSION_KEY]
    return {"menu_list": menu_list}


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    '''
    创建二级菜单
    :return:
    '''
    menu_dict = request.session[settings.MENU_SISSION_KEY]

    # print(request.current_selected_permission,type(request.current_selected_permission))
    # 对字典的key进行排序
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()
    for key in key_list:
        val = menu_dict[key]
        val['class'] = 'hide'
        # for per in val['children']:
        #     regex = '%s$'% ([per['url']])
        #     if re.match(regex, request.path_info):
        #         per['class'] = 'active'
        #         val['class'] = ''
        # ordered_dict[key] = val
        for per in val['children']:
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
        ordered_dict[key] = val

    return {"menu_dict": ordered_dict}


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    return {'record_list': request.breadcrumb}


@register.filter
def has_permission(request, name):
    """
    判断是否有权限
    :param request:
    :param name:
    :return:
    """
    if name in request.session[settings.PERMISSION_SISSION_KEY]:
        return True


@register.simple_tag
def memory_cul(request, name, *args, **kwargs):
    '''
    生成带有搜索条件的URL(替代了模板中的URL)
    :param request:
    :param name:
    :return:
    '''
    # basic_url = reverse(name, args=args, kwargs=kwargs)
    #
    # # 当前URL中无参数
    # if not request.GET:
    #     return basic_url
    #
    # query_dict = QueryDict(mutable=True)
    # query_dict['_filter'] = request.GET.urlencode()
    # # query_dict.urlencode() # filter=mid=26&age=99
    #
    # return "%s?%s" % (basic_url, query_dict.urlencode())
    return Menu_urls.memory_cul(request, name, *args, **kwargs)