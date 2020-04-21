from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.


class User(AbstractUser):
    # 用户信息
    id = models.AutoField(primary_key = True)
    telephone = models.CharField(max_length=11,null=True,unique=True)
    email = models.EmailField()
    avatar = models.FileField(upload_to='static/image/', default="/static/image/default.jpg")
    create_time = models.DateField(verbose_name='创建时间',auto_now_add=True)
    blog = models.OneToOneField(to='Blog',to_field='id',on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.username


class Blog(models.Model):
    # 博客信息
    id = models.AutoField(primary_key = True)
    title = models.CharField(verbose_name='博客标题',max_length=99)
    site_name = models.CharField(verbose_name='站点名',max_length=99)

    def __str__(self):
        return self.title


class Category(models.Model):
    # 分类
    id = models.AutoField(primary_key = True)
    blogs = models.ForeignKey(verbose_name='所属博客',to='Blog',to_field='id',on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题',max_length=99)

    def __str__(self):
        return self.title


class Tag(models.Model):
    # 标签
    id = models.AutoField(primary_key=True)
    title = models.CharField(verbose_name='标签名称', max_length=32)
    blogs = models.ForeignKey(verbose_name='所属博客', to='Blog', to_field='id', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Article(models.Model):
    # 文章
    id = models.AutoField(primary_key = True)
    title = models.CharField(max_length=50, verbose_name='文章标题')
    desc = models.CharField(max_length=255, verbose_name='文章描述')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    content = models.TextField()
    comment_count = models.IntegerField(default=0)
    up_count = models.IntegerField(default=0)
    down_count = models.IntegerField(default=0)
    user = models.ForeignKey(verbose_name='作者', to='User', to_field='id', on_delete=models.CASCADE)
    category = models.ForeignKey(to='Category', to_field='id', null=True, on_delete=models.CASCADE)
    tags = models.ManyToManyField(to="Tag",through='Article_Tag',through_fields=('article', 'tags'),)

    def __str__(self):
        return self.title


class Article_Tag(models.Model):
    # 文章-标签关系表
    id = models.AutoField(primary_key = True)
    article = models.ForeignKey(to='Article',to_field='id',on_delete=models.CASCADE)
    tags = models.ForeignKey(to='Tag',to_field='id',on_delete=models.CASCADE)

    class Meta:
        unique_together = [('article','tags'),]

    def __str__(self):
        return self.article.title + '-----' + self.tags.title


class ArticleUpDown(models.Model):
    # 点赞表
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', null=True, on_delete=models.CASCADE)
    article = models.ForeignKey("Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = [
            ('article', 'user'),
        ]


class Comment(models.Model):
    # 评论表
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(verbose_name='评论文章', to='Article', to_field='id', on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name='评论者', to='User', to_field='id', on_delete=models.CASCADE)
    content = models.CharField(verbose_name='评论内容', max_length=255)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    parent_comment = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content