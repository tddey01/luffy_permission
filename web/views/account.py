#!/usr/bin/env  python3
# coding utf-8

from django.shortcuts import HttpResponse, render,redirect
from rbac import models
from rbac.services.init_permission import  init_permissions


def login(request):
    # print(request.POST)
    # 1 用户登录
    if request.method == "GET":
        return render(request, 'login.html')
    user = request.POST.get('user')
    pwd = request.POST.get('pwd')

    curent_user = models.UserInfo.objects.filter(name=user, password=pwd).first()
    if not curent_user:
        return render(request, 'login.html', {'msg': '用户密码错误'})
    # # 2  用户权限初始化
    # # 根据当前用户信息获取此用户所拥有的的所有权限  并放入到session中
    # # 当前用户所有权限
    # permission_queryest =  curent_user.roles.filter(permissions__isnull=False).values('permissions__id','permissions__url').distinct()
    # # permission_list = curent_user.roles.all().values('permissions__id', 'permissions__url').distinct()
    # # print(permission_list)
    #
    #
    # # 获取权限中所有的URL
    # # permissions_list = []
    # # for item in permission_queryest:
    # #     permissions_list.append(item['permissions__url'])
    # #     # print(item)
    # #     print(permissions_list)
    # # print('______')
    # permission_list = [item['permissions__url'] for item in permission_queryest]
    #
    # # print(permission_list)
    #
    #
    # request.session['luffy_permission_list_url_list'] = permission_list

    # return HttpResponse('ok')
    init_permissions(curent_user,request)
    return redirect('/customer/list/')
    # 根据当前用户信息 获取此用户拥有的权限 并放到session中
