#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django.conf.urls import url,include
from rbac.views import role
app_name = 'rbac'
urlpatterns = [
    url(r'^role/list/$',role.role_list,name='role_list'),  # rbac:role_list
    url(r'^role/add/$', role.role_add,name='role_add'), # rbac:role_add
    url(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),  # rbac:role_del
    url(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),  # rbac:role_edit



]