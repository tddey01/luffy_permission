#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
'''
用户管理
'''

from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from rbac import models
from rbac.forms.User import UserModelForms
from rbac.forms.User import UpdateUserModelForms
from rbac.forms.User import ResetpassUserModelForms


def user_list(request):
    '''
    用户列表
    :param request:
    :return:
    '''
    user_queryse = models.UserInfo.objects.all()
    return render(request, 'rbac/user_list.html', {'users': user_queryse})


def user_add(request):
    '''
    添加用户
    :param request:
    :return:
    '''
    if request.method == 'GET':
        form = UserModelForms()
        return render(request, 'rbac/change.html', {'form': form})
    form = UserModelForms(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    '''
    修改用户和邮箱
    :param request:
    :param pk:
    :return:
    '''
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UpdateUserModelForms(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = UpdateUserModelForms(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_reset_password(request, pk):
    '''
    重置用户密码
    :param request:
    :param pk:
    :return:
    '''
    obj = models.UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == "GET":
        form = ResetpassUserModelForms()
        return render(request, 'rbac/change.html', {'form': form})
    form = ResetpassUserModelForms(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))
    return render(request, 'rbac/change.html', {'form': form})


def user_del(request, pk):
    '''
    删除用户
    :param request:
    :param pk:
    :return:
    '''
    # origin_url = reverse('rbac:user_list')
    # if request.method == 'GTE':
    #     return render(request, 'rbac/delete.html', {'cancel_url': origin_url})
    #
    # models.UserInfo.objects.filter(id=pk).delete()
    #
    # return redirect(origin_url)
    qrigin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': qrigin_url})

    models.UserInfo.objects.filter(id=pk).delete()
    return  redirect(qrigin_url)
