#!/usr/bin/env  python3
# -*- coding: UTF-8 -*-
from django import forms
from rbac import models
class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['title', ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'})
        }