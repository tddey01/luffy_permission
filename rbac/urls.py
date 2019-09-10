#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django.conf.urls import url,include
from rbac.views import role
from rbac.views import user
from rbac.views import  menu
app_name = 'rbac'
urlpatterns = [
    url(r'^role/list/$',role.role_list,name='role_list'),  # rbac:role_list
    url(r'^role/add/$', role.role_add,name='role_add'), # rbac:role_add
    url(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  # rbac:role_del
    url(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),  # rbac:role_edit
    url(r'^user/list/$', user.user_list, name='user_list'),  # rbac:user_list
    url(r'^user/add/$', user.user_add, name='user_add'), # rbac:user_add
    url(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),  # rbac:user_del
    url(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_password, name='user_reset_password'),  # rbac:user_password  重置密码
    url(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),  # rbac:user_edit
    url(r'^menu/list/$', menu.menu_list, name='menu_list'),  # rbac:menu_list
    url(r'^menu/add/$', menu.menu_add, name='menu_add'),  # rbac:menu_add



]