#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.forms import formset_factory

# from django.urls import reverse
from rbac import models
from rbac.forms.Menu import MenuModelForms
from rbac.forms.Menu import SecondMenuModelForms
from rbac.forms.Menu import PermissionModelForms
from rbac.forms.Menu import MultiAddPermissionForm
from rbac.forms.Menu import MultiEditPermissionForm
from rbac.services.Menu_urls import memory_resverse
from rbac.services.routes import get_all_url_dict
from collections import OrderedDict


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


def multi_permissions(request):
    """
    批量操作权限
    :param request:
    :return:
    """

    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    # 1. 获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    """
    {
        'rbac:role_list':{'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        'rbac:role_add':{'name': 'rbac:role_add', 'url': '/rbac/role/add/'},
        ....
    }
    """
    router_name_set = set(all_url_dict.keys())

    # 2. 获取数据库中所有的URL
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    print(permissions)
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])
    """
    {
        'rbac:role_list': {'id':1,'title':'角色列表',name:'rbac:role_list',url.....},
        'rbac:role_add': {'id':1,'title':'添加角色',name:'rbac:role_add',url.....},
        ...
    }
    """

    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)  # {'name': 'rbac:role_list', 'url': '/rbac/role/list/'},
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3. 应该添加、删除、修改的权限有哪些？
    # 3.1 计算出应该增加的name

    generate_name_list = router_name_set - permission_name_set
    generate_formset = generate_formset_class(
        initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name

    update_name_list = permission_name_set & router_name_set
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    return render(
        request,
        'rbac/multi_permsissions.html',
        {
            'generate_formset': generate_formset,
        }
    )