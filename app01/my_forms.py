#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Mr.Zhang"
# Date: 2020/4/9

#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Mr.Zhang"
# Date: 2020/4/9

from django.core.exceptions import ValidationError
from django import forms
from django.forms import widgets

from app01.models import User


class register(forms.Form):
    username = forms.CharField(label='用户',widget=widgets.TextInput(attrs={"class":"form-control"}))
    password = forms.CharField(label='密码',widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    nickname = forms.CharField(label="昵称",widget=widgets.TextInput(attrs={"class":"form-control"}))
    confirm_password = forms.CharField(label='确认密码',widget=widgets.PasswordInput(attrs={"class":"form-control"}))
    telephone = forms.CharField(label='手机号码',widget=widgets.TextInput(attrs={"class":"form-control"}))
    email = forms.CharField(label='邮箱',widget=widgets.EmailInput(attrs={"class":"form-control"}))

    def clean_username(self):
        name = self.cleaned_data.get('username')
        if User.objects.filter(username=name):
            raise ValidationError('用户名已注册！')
        else:
            return name

    def clean_telephone(self):
        tel = self.cleaned_data.get('telephone')
        if  not tel.isdigit():
            raise ValidationError('手机号不合法！')
        elif User.objects.filter(telephone=tel):
            raise ValidationError('该手机号已注册！')
        else:
            return tel

    def clean(self):
        val1 = self.cleaned_data.get('password')
        val2 = self.cleaned_data.get('confirm_password')
        if val1 != val2:
            raise ValidationError('确认密码不一致！')
        else:
            return self.cleaned_data






