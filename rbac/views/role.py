#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
'''
角色管理
'''
from django.shortcuts import render, redirect,HttpResponse
from django.urls import reverse
from django import forms
from rbac import models


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }


def role_list(request):
    '''
    角色列表
    :param requst:
    :return:
    '''
    role_queryset = models.Role.objects.all()

    return render(request, 'rbac/role_list.html', {'roles': role_queryset})


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()
        return render(request, 'rbac/change.html', {'form': form})

    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(request, 'rbac/change.html', {'form': form})


def role_edit(request,pk):
    '''
    编辑角色
    :param request:
    :param pk: 修改角色id
    :return:
    '''
    obj = models.Role.objects.filter(id=pk).first()

    if not  obj:
        return HttpResponse('角色不存在')

    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(request,'rbac/change.html',{'form':form})
    form = RoleModelForm(instance=obj,data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))
    return render(request,'rbac/change.html',{'fom':form})



def role_del(request,pk):

    pass