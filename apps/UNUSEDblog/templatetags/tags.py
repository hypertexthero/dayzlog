# http://www.mechanicalgirl.com/post/custom-template-tags-in-django/
from blog.models import Post
from django import template

register = template.Library()

def latestpost(context): # need 'context' in here otherwise get 'list index out of range' error
    posts = Post.objects.all().order_by('-modified', 'title')[:1]
    # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    user = context['request'].user
    return {'posts': posts, 'user': user}

register.inclusion_tag('includes/latestpost.html', takes_context=True)(latestpost) # needed to add 'takes_context=True' argument so that the user variable would get passed into the context

