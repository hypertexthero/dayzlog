# http://www.mechanicalgirl.com/post/custom-template-tags-in-django/
from notes.models import Note
from django import template

register = template.Library()

def latestnote(context): # need 'context' in here otherwise get 'list index out of range' error
    notes = Note.objects.all().order_by('-modified', 'title')[:1]
    # http://stackoverflow.com/a/4338108/412329 - passing the user variable into the context
    user = context['request'].user
    return {'notes': notes, 'user': user}

register.inclusion_tag('includes/latestnote.html', takes_context=True)(latestnote) # needed to add 'takes_context=True' argument so that the user variable would get passed into the context

