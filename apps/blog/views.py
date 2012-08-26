from datetime import datetime

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic import date_based, list_detail
from django.conf import settings
from django.db.models import Q

from misc.json_encode import json_response
from blog.models import Post, IS_DRAFT, IS_PUBLIC
from blog.forms import PostForm
from blog.signals import post_published

# homepage
from django.views.generic.date_based import archive_index
from django.views.generic.list_detail import object_list

def blog_post_detail(request, *kargs, **kwargs):
    blog = get_object_or_404(Blog, slug = kwargs.pop('blog', ''))
    kwargs['template_object_name'] = 'post'
    kwargs['queryset'] = Post.objects.filter(blog = blog)
    if request.user.is_authenticated():
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user) | kwargs['queryset'].filter(status=IS_PUBLIC)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(status=IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

def blog_user_post_detail(request, *kargs, **kwargs):
    user = get_object_or_404(User, username=kwargs.pop('username', ''))
    # =todo: show vote on post detail page
    # vote = get_object_or_404(Vote, int(0))
    if user==request.user:
        kwargs['queryset'] = kwargs['queryset'].filter(author=request.user)
    else:
        kwargs['queryset'] = kwargs['queryset'].filter(author=user, status=IS_PUBLIC)
    return list_detail.object_detail(request, *kargs, **kwargs)

def user_post_list(request, *kargs, **kwargs):
    user = get_object_or_404(User, username = kwargs.pop('username', ''))
    kwargs['queryset'] = kwargs['queryset'].filter(author=user)
    kwargs['extra_context'] = {'current_user': user, 'author': user}
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def my_post_list(request, *kargs, **kwargs):
    # kwargs['queryset'] = Post.objects.filter(author = request.user).exclude(status = IS_DELETED)
    kwargs['queryset'] = Post.objects.filter(author = request.user)
    return list_detail.object_list(request, *kargs, **kwargs)

@login_required
def change_status(request, action, id):
    post = get_object_or_404(Post, pk = id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't change statuses of posts that aren't yours")
    else:
        if action == 'draft' and post.status == IS_PUBLIC:
            post.status = IS_DRAFT
        if action == 'public' and post.status == IS_DRAFT:
            post.status = IS_PUBLIC
            post_published.send(sender=Post, post=post)
        post.save()
        request.user.message_set.create(message=_("Successfully change status for post '%s'") % post.title)
    return redirect("blog_my_post_list")

@login_required
def add(request, form_class=PostForm, template_name="blog/post_add.html"):
    post_form = form_class(request)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.author = request.user
        creator_ip = request.META.get('HTTP_X_FORWARDED_FOR', None)
        if not creator_ip:
            creator_ip = request.META.get('REMOTE_ADDR', None)
        post.creator_ip = creator_ip
        post.save()
        request.user.message_set.create(message=_("Successfully created post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form}, context_instance=RequestContext(request))

@login_required
def edit(request, id, form_class=PostForm, template_name="blog/post_edit.html"):
    post = get_object_or_404(Post, id=id)
    if post.author != request.user:
        request.user.message_set.create(message="You can't edit posts that aren't yours")
        return redirect("blog_my_post_list")
    post_form = form_class(request, instance=post)
    if request.method == "POST" and post_form.is_valid():
        post = post_form.save(commit=False)
        post.updated_at = datetime.now()
        post.save()
        request.user.message_set.create(message=_("Successfully updated post '%s'") % post.title)
        return redirect("blog_user_post_detail", username=request.user.username, slug=post.slug)
    return render_to_response(template_name, {"post_form": post_form, "post": post}, context_instance=RequestContext(request))

# delete entry
from django.views.generic.create_update import delete_object
@login_required
def delete(request, id):
    """Delete a post based on id"""

    return delete_object(request,
        model=Post,
        object_id=id,
        template_object_name='post', # so I can write {{ note.title }} in templates/notes/delete.html (otherwise I would need to write {{ object.title }})
        template_name='blog/post_delete.html',
        post_delete_redirect=reverse("blog_my_post_list")
    )

# =todo: export all posts to plain text in markdown format
# https://docs.djangoproject.com/en/1.0/topics/generic-views/#performing-extra-work
# def posts_plaintext(request):
#     response = list_detail.object_list(
#         request,
#         queryset = Post.objects.all(),
#         mimetype = "text/plain",
#         template_name = "blog/posts_plaintext.txt"
#     )
#     response["Content-Disposition"] = "attachment; filename=MyDayZLogPosts.txt"
#     return response

def homepage(request): 
    """Show top posts"""
    return object_list(request, 
        # http://eflorenzano.com/blog/2008/05/24/managers-and-voting-and-subqueries-oh-my/
        queryset=Post.hot.most_loved().filter(status=IS_PUBLIC), # .annotate(num_votes=Count('score')) 
        template_name='homepage.html',
        template_object_name='post',
        # extra_context={'profile': profile}
    )

def new(request): 
    """Show new posts"""
    return object_list(request, 
        queryset=Post.objects.filter(status=IS_PUBLIC).order_by('-created_at'), 
        template_name='new.html',
        template_object_name='post',
    )