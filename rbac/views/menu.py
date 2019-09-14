#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django.shortcuts import HttpResponse, redirect, render
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string

# from django.urls import reverse
from rbac import models
from rbac.forms.Menu import MenuModelForms
from rbac.forms.Menu import SecondMenuModelForms
from rbac.forms.Menu import PermissionModelForms
from rbac.services.Menu_urls import memory_resverse




def menu_list(request):
    '''
    菜单和权限列表
    :param request:
    :return:
    '''

    menus = models.Menu.objects.all()

    menu_id = request.GET.get('mid')  # 用户选择的一级菜单
    second_menu_id = request.GET.get('sid')  # 用户选择的二级菜单

    menu_exists = models.Menu.objects.filter(id=menu_id).exists()  # 查看标的id
    if not menu_exists:
        menu_id = None

    if menu_id:
        second_menu = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menu = []

    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()  # 查看标的id
    if not second_menu_exists:
        second_menu_id = None

    if second_menu_id:
        permission = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permission = []

    return render(
        request, 'rbac/menu_list.html',
        {
            'menus': menus,
            'second_menu': second_menu,
            'permission': permission,
            'menu_id': menu_id,
            'second_menu_id': second_menu_id,
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


def second_menu_add(request, menu_id):
    """
    添加二级菜单
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()  # 取到menu_id对象

    if request.method == 'GET':
        form = SecondMenuModelForms(initial={'menu': menu_object})
        return render(request, 'rbac/change.html', {'form': form})

    form = SecondMenuModelForms(data=request.POST)
    if form.is_valid():
        form.save()

        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_edit(request, pk):
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

    form = SecondMenuModelForms(data=request.POST, instance=Permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def second_menu_del(request, pk):
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


def permission_add(request, second_menu_id):
    '''
    添加权限菜单
    :param request:
    :return:
    '''

    if request.method == 'GET':
        form = PermissionModelForms()
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForms(data=request.POST)
    if form.is_valid():
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()  # 取到menu_id对象

        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择')
        # form instance 中包含用户提交的所有数据

        form.instance.pid = second_menu_object

        # instance = models.Permission(title='',name='',url='',pid=second_menu_object)
        # instance.pid = second_menu_object
        # instance.save()

        form.save()
        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_edit(request, pk):
    '''
     编辑权限
    :param request:
    :param pk:当前要编辑的权限ID
    :return:
    '''
    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForms(instance=permission_object)
        return render(request, 'rbac/change.html', {'form': form})

    form = PermissionModelForms(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_resverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/change.html', {'form': form})


def permission_del(request, pk):
   '''
    删除权限
   :param request:
   :param pk:
   :return:
   '''

   url = memory_resverse(request, 'rbac:menu_list')
   if request.method == 'GET':
       return render(request, 'rbac/delete.html', {'cancel_url': url})

   models.Permission.objects.filter(id=pk).delete()
   return redirect(url)

def recursion_urls(pre_namespace,pre_url,urlpatterns,url_ordered_dict):
    '''
    递归的获取URL
    :param pre_namespace:   namespace 前缀 以后用于拼接前缀 name
    :param pre_url:     url 前缀  以后用于拼接 url
    :param urlpatterns:   路由关系列表
    :param url_ordered_dict:  用于保存递归中获取的所有路由
    :return:
    '''


def  get_all_url_dic():
    '''
    获取项目中所有的URL
    :return:
    '''
    url_ordered_dict = OrderedDict()
    '''
    {
        'rbac:menu_list':{
        name:'rbac:menu_list'
        url;'xxx/xxx/menu/list',
        }
    }
    '''
    md = import_string(settings.ROOT_URLCONF)  # from luff .. import urls

    # for item in md.urlpatterns:
    #     print(item)
    recursion_urls(None , '/', md.urlpatterns, url_ordered_dict)



def multi_permission(request,):
    '''
    批量操作权限
    :param request:
   :param second_menu_id:
    :return:
    '''
    get_all_url_dic()
    return  HttpResponse('ok')
