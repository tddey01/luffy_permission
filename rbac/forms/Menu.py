#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django import forms

from rbac import  models


class MenuModelForms(forms.ModelForm):
    class Meta:
        model = models.Menu
        fields = '__all__'