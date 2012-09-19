# -*- coding: utf-8 -*-
import re

from django import template
from django.conf import settings
from django.template import Variable
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.template import RequestContext

from dayzlog.apps.blog.models import Post, IS_DRAFT, IS_PUBLIC

register = template.Library()

@register.tag
def check_post_status(parser, token):
    bits = token.contents.split(' ')
    return CheckPostStatus(bits[1], bits[2])

class CheckPostStatus(template.Node):
    def __init__(self, user, post):
        self.user = user
        self.post = post

    def render(self, context):
        user = Variable(self.user).resolve(context)
        post = Variable(self.post).resolve(context)
        if not user or not post:
            return ''
        if post.author == user or post.status == IS_PUBLIC:
            context['show_post'] = True
        else:
            context['show_post'] = False
        return ''

@register.inclusion_tag("blog/post_item.html", takes_context = True)
def show_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = True
    return context

@register.inclusion_tag("blog/post_item.html", takes_context = True)
def show_full_blog_post(context, post):
    context['post'] = post
    context['post_undetailed'] = False
    return context


@register.simple_tag
def active(request, pattern):
    if re.search(pattern, request.path):
        return ' class="active"'
    return ''

# http://stackoverflow.com/a/9250304
@register.filter
def tabindex(value, index):
    """
    Add a tabindex attribute to the widget for a bound field.
    """
    value.field.widget.attrs['tabindex'] = index
    return value

# http://djangosnippets.org/snippets/2019/
# from django.db.models.loading import get_model
# from django.db.models.query import QuerySet
# 
# @register.filter
# def call_manager(model_or_obj, method):
#     # load up the model if we were given a string
#     if isinstance(model_or_obj, basestring):
#         model_or_obj = get_model(*model_or_obj.split('.'))
# 
#     # figure out the manager to query
#     if isinstance(model_or_obj, QuerySet):
#         manager = model_or_obj
#         model_or_obj = model_or_obj.model
#     else:
#         manager = model_or_obj._default_manager
# 
#     return getattr(manager, method)()