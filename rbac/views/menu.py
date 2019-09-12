#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django.shortcuts import HttpResponse, redirect, render
# from django.urls import reverse
from rbac.forms.Menu import MenuModelForms
from rbac.forms.Menu import SecondMenuModelForms
from rbac.services.Menu_urls import memory_resverse
from rbac import models


def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''

    menus = models.Menu.objects.all()

    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menu_exists= models.Menu.objects.filter(id=menu_id).exists()  #查看标的id
    if not menu_exists:
        menu_id = None

    if menu_id:
        second_menu = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menu = []
    return render(
        request, 'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menu': second_menu,
            'menu_id': menu_id,
            'second_menu_id':second_menu_id,

        })


def menu_add(request):
    """
    添加一级菜单
    :param request:
    :return:
    """

    if request.method == 'GET':
        form = MenuModelForms()
        return render(request, 'rbac/change.html', {'form': form})

    form = MenuModelForms(data=request.POST)
    if form.is_valid():
        form.save()
        # url = reverse('rbac:menu_list')
        # origin_params = request.GET.get("_filter")
        # if origin_params:
        #     url = "%s?%s" %(url,origin_params)

        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def menu_edit(request, pk):
    '''
    修改编辑菜单
    :param request:
    :param pk:
    :return:
    '''

    obj = models.Menu.objects.filter(id=pk).first()

    if not obj:
        return HttpResponse('菜单不存在')

    if request.method == 'GET':
        form = MenuModelForms(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})
    form = MenuModelForms(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        # url = reverse('rbac:menu_list')
        # origin_params = request.GET.get("_filter")
        # if origin_params:
        #     url = "%s?%s" %(url,origin_params)
        # return redirect(url)
        return redirect(memory_resverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})


def menu_del(request, pk):
    '''
    删除菜单
    :param request:
    :param pk:
    :return:
    '''

    # url = reverse('rbac:menu_list')
    # origin_params = request.GET.get("_filter")
    # if origin_params:
    #     url = "%s?%s" % (url, origin_params)
    url = memory_resverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': url})

    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request,menu_id):

    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()  #取到menu_id对象


    if request.method == 'GET':
        form = SecondMenuModelForms(initial={'menu':menu_object})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForms(data=request.POST)
    if form.is_valid():
        form.save()

        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})



def second_menu_edit(request,pk ):

    '''
    编辑二级菜单
    :param request:
    :param pk:
    :return:
    '''

    Permission_object = models.Permission.objects.filter(id=pk).first()
    if request.method == 'GET':
        form = SecondMenuModelForms(instance=Permission_object)
        return render(request, 'rbac/change.html', {'form': form})
    form = SecondMenuModelForms(data=request.POST,instance=Permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_resverse(request, 'rbac:menu_list'))
    return render(request, 'rbac/change.html', {'form': form})

def second_menu_del(request,pk ):
    '''
    删除二级菜单
    :param request:
    :param pk:
    :return:
    '''
    url = memory_resverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': url})
    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)