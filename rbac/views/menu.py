#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from  django.shortcuts import HttpResponse,redirect,render

def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''
    return  render(request,'rbac/menu_list.html')


def  menu_add(request):
    pass
