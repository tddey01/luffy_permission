#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django import forms
from django.core.exceptions import ValidationError
from rbac import models


class UserModelForms(forms.ModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

        # 手动配置错误提示
        # error_messages = {
        #     'name':{'required':'用户名不能为空'},
        #     'email': {'required': '邮箱不能为空'},
        #     'password': {'required': '密码不能为空'},
        #     'confirm_password': {'required': '确认密码不能为空'},
        # }

    def __init__(self, *args, **kwargs):
        super(UserModelForms, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        '''
        两次密码不一致
        :return:
        '''
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码不一致')
        return confirm_password


class UpdateUserModelForms(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email',]

    def __init__(self, *args, **kwargs):
        '''
        定义样式
        :param args:
        :param kwargs:
        '''
        super(UpdateUserModelForms, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ResetpassUserModelForms(forms.ModelForm):
    confirm_password = forms.CharField(label='修改密码')

    class Meta:
        model = models.UserInfo
        fields = ['password','confirm_password']

        # 手动配置错误提示
        # error_messages = {
        #     'name':{'required':'用户名不能为空'},
        #     'email': {'required': '邮箱不能为空'},
        #     'password': {'required': '密码不能为空'},
        #     'confirm_password': {'required': '确认密码不能为空'},
        # }

    def __init__(self, *args, **kwargs):
        super(ResetpassUserModelForms, self).__init__(*args, **kwargs)
        # 统一给ModelForm生成字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean_confirm_password(self):
        '''
        两次密码不一致
        :return:
        '''
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码不一致')
        return confirm_password
