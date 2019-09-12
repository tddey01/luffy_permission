#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-

from django import forms

class BootStrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        '''
        样式钩子方法
        :param args:
        :param kwargs:
        '''

        super(BootStrapModelForm, self).__init__(*args, **kwargs)
        # 统一ModelForm生成不同字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'