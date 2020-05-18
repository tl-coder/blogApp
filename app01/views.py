import os
import random
import sys
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.contrib import auth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from app01.my_forms import *
from app01.models import *

# 首页
def index(request):
    return render(request,'index.html')

# 注销
def logout(requset):
    auth.logout(requset)
    return redirect("/index")

# 注册
def sign_up(request):
    if request.method == 'POST':
        response = {"user":None,"msg":None}
        form = register(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('username')
            psw = form.cleaned_data.get('password')
            tel = form.cleaned_data.get('telephone')
            email = form.cleaned_data.get('email')
            avatar_obj = request.FILES.get("avatar")
            if avatar_obj:
                User.objects.create_user(username=user,password=psw,telephone=tel,email=email,avatar=avatar_obj)
            else:
                User.objects.create_user(username=user,password=psw,telephone=tel,email=email)
            response['user'] = user
        else:
            error_msg = form.errors
            response['msg'] = error_msg
        return JsonResponse(response)
    form = register()
    return render(request,'register.html',locals())


#登录
def sign_in(request):
    if request.method == 'GET':
        return render(request,'login.html')
    elif request.method == 'POST':
        response = {"user": None, "msg": None}
        name = request.POST.get('username')
        psw = request.POST.get('password')
        valid_code = request.POST.get('valid_code')
        valid_code_str = request.session["valid_code_str"]
        if valid_code_str.upper() == valid_code.upper():  #校验码是否一致,upper()：字母大写转换小写
            user = auth.authenticate(username=name,password=psw)
            if user is not None:
                auth.login(request,user)
                response['user'] = user.username
                print('控制台：登陆成功')
            else:
                response['msg'] = '用户名或者密码不正确！'
        else:
            response["msg"] = "验证码错误!"
        return JsonResponse(response)

# 验证码
def get_validCode_img(request):
    img = Image.new("RGB",(120,60),color="red")
    draw = ImageDraw.Draw(img)   # 画板
    valid_code_str = ""
    kumo_font = ImageFont.truetype(font="static/font/FZQiTi-S14S.TTF",size=32)
    for i in range(5):
        random_int = str(random.randint(0,9))
        random_abc = chr(random.randint(97,122))
        random_ABC = chr(random.randint(65,90))
        valid_code = random.choice([random_int,random_abc,random_ABC])
        draw.text((i*24,5),valid_code,font=kumo_font)   # 验证码
        valid_code_str += valid_code
    request.session["valid_code_str"] = valid_code_str
    f = BytesIO()
    img.save(f,'png')
    data = f.getvalue()
    return HttpResponse(data)

