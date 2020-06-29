from django import template
from django.db.models import Count
from app01.models import *
register=template.Library()


@register.inclusion_tag("aside_homesite.html")
def get_aside_style(user):
    # 最新文章列表
    top_list = user.article_set.order_by('create_time').all()
    blog = user.blog
    # 标签列表
    tag_list = Tag.objects.filter(blogs=blog).values('id').annotate(c=Count('article')).values('title','c','id')
    return {"top_list":top_list,"tag_list":tag_list,"user":user}