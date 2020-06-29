import random
import time
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from django.contrib import auth
from django.db import transaction
from django.db.models import *
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from app01.my_forms import *
from app01.models import *


# 首页
def index(request):
    art_list = Article.objects.all().order_by('-create_time')
    return render(request,'index.html',locals())


# 注销
def logout(request):
    auth.logout(request)
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


# 登录
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


# 个人播客主页
def blog_mainPage(request,**kwargs):
    user = User.objects.filter(username = kwargs['username']).first()
    # 个人站点跳转
    # 标签分类
    if kwargs.get('condition',0):
        if kwargs['condition'] == 'tag':
            article_list = Article.objects.filter(tags=kwargs['key'])
    # 个人站点
    else:
        if not user:
            return render(request,"404.html")
        # 文章列表
        article_list = user.article_set.all().order_by('create_time')
    return render(request,"homesite.html",locals())


# 文章详情页
def article_detail(request,**kwargs):
    user = User.objects.filter(username=kwargs['username']).first()
    article_view = Article.objects.filter(id=kwargs['article_id']).first()
    updown_obj = ArticleUpDown.objects.filter(user=request.user,article=article_view).first()
    login_user = request.user
    comment_list = comment_list_obj(article_id=kwargs.get("article_id"))
    return render(request,"article_detail.html",locals())


# 点赞
def article_up(request):
    response={"status":None}
    art_ud = ArticleUpDown.objects.filter(user=request.user,article=request.POST.get('article_id'))
    article = Article.objects.filter(id=request.POST.get('article_id'))
    if art_ud:
        art_ud.delete()
        article.update(up_count = F("up_count")-1)
        response['status'] = False
    else:
        ArticleUpDown.objects.create(user=request.user,article=article.first())
        article.update(up_count = F("up_count")+1)
        response['status'] = True
    return JsonResponse(response)


# 评论
def article_comment(request):
    response = {'create_time':None,'parent_comment':None,'article_id':None}
    with transaction.atomic():   #事务，sql操作数据库，错误则回滚
        user = request.user
        article = Article.objects.filter(id=request.GET.get("article_id")).first()
        content = request.GET.get("content")
        parent_comment_id = request.GET.get("parent_comment")
        parent_comment = None
        if parent_comment_id:
            parent_comment_id = int(parent_comment_id)
            parent_comment = Comment.objects.filter(nid=parent_comment_id).first()
        create_time = time.strftime("%Y-%M-%D",time.gmtime())
        Comment.objects.create(user=user,article=article,content=content,parent_comment=parent_comment,create_time=create_time)
        Article.objects.filter(id=request.GET.get('article_id')).update(comment_count=F("comment_count")+1)
    response['create_time'] = create_time
    response['parent_comment'] = request.GET.get('parent_comment')
    response['article_id'] = request.GET.get('article_id')
    return JsonResponse(response)

# 评论列表构造体
def comment_list_obj(**kwargs):
    comment_list = {}
    list = Comment.objects.filter(article=kwargs.get("article_id")).order_by('create_time')
    for comment in list:
        if not comment.parent_comment:
            comment_list[comment.nid] = {
                "user":comment.user,
                "content":comment.content,
                "create_time":comment.create_time,
                "son_comment":[]
            }
        else:
            comment_list[comment.parent_comment.nid]['son_comment'].append({
                "user":comment.user,
                "content":comment.content,
                "create_time":comment.create_time
            })
    return comment_list

# 评论树
def tree_comment(request):
    comment_list = comment_list_obj(article_id=request.POST.get("article_id"))
    return render(request,"tree_comment.html",locals())