#!/usr/bin/env  python3
# coding utf-8

from django.shortcuts import HttpResponse, render
from rbac.models import UserInfo


def login(request):

    print(request.POST)
    if request.method == "POST":
        return render(request, 'login.html')
