"""blogApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.views.static import serve
from app01 import views
from blogApp import settings

urlpatterns = [
    # 超级管理员
    path('admin/',admin.site.urls),
    # 首页  127.0.0.1:8000
    re_path('^$',views.index),
    # 首页  127.0.0.1:8000/index
    path('index/',views.index,name='index'),
    # 注册
    path('register/',views.sign_up,name='register'),
    # 登录
    path('login/',views.sign_in,name='login'),
    # 登出
    path('logout/',views.logout,name='logout'),
    # 验证码
    path('get_validCode_img/',views.get_validCode_img,name='static_image'),
    # 静态文件访问
    re_path(r"media/(?P<path>.*)$",serve,{"document_root":settings.MEDIA_ROOT}),
    # 点赞
    re_path("^article_up/$",views.article_up),
    # 评论
    re_path("^save_comment/$",views.article_comment),
    # 评论树
    re_path("^tree_comment/$",views.tree_comment),
    # 个人博客主页
    re_path("^(?P<username>\w+)/$",views.blog_mainPage),
    # 个人博客二级跳转
    re_path("^(?P<username>\w+)/(?P<condition>category|tag)/(?P<key>.*)/$",views.blog_mainPage),
    #文章详情
    re_path("^(?P<username>.*)/articles/(?P<article_id>.*)/$",views.article_detail),



]
