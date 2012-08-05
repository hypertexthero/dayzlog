# -*- coding: utf-8 -*-
from django import template
from django.template import Variable
from django.conf import settings

DEFAULT_WINDOW = getattr(settings, 'PAGINATION_DEFAULT_WINDOW', 4)

register = template.Library()

@register.tag
def get_dict(parser, token):
    """
        Call {% get_dict dict key default_key %} or {% get_dict dict key %}
        Return value from dict of key element. If there are no key in get_dict it returns default_key (or '')
        Return value will be in parameter 'value'
    """
    bits = token.contents.split(' ')
    return GetDict(bits[1], bits[2], ((len(bits) > 3) and bits[3]) or '')

class GetDict(template.Node):
    def __init__(self, dict, key, default):
        self.dict = dict
        self.key = key
        self.default = default

    def render(self, context):
        dict = Variable(self.dict).resolve(context)
        key = context.get(self.key, self.key)
        default = context.get(self.default, self.default)
        if dict:
            context['value'] = dict.get(key, default)
        else:
            context['value'] = default
        return ''

@register.tag
def define(parser, token):
    """
        Call {% define variable key %}
        This tag save content of variable in key.
    """
    bits = token.contents.split(' ')
    return Define(bits[1], bits[2])

class Define(template.Node):
    def __init__(self, value, key):
        self.value = value
        self.key = key

    def render(self, context):
        value = Variable(self.value).resolve(context)
        context[self.key] = value
        return ''

@register.tag
def sort_by(parser, token):
    bits = token.contents.split(' ')
    return SortBy(bits[1], bits[2], bits[3])

class SortBy(template.Node):
    def __init__(self, query, default_sort, name_of_result):
        self.query = query
        self.default_sort = default_sort
        self.name_of_result = name_of_result

    def render(self, context):
        query = Variable(self.query).resolve(context)
        if 'request' in context and query:
            request = context['request']
            sort = request.GET.get('sort', self.default_sort)
            context['sort'] = sort
            if 'sort_dict' in context:
                sort_dict = context['sort_dict']
            if sort and sort_dict and sort in sort_dict:
                context[self.name_of_result] = query.order_by(sort_dict[sort])
        return ''

def paginate(context, window=DEFAULT_WINDOW):
    """
    Renders the ``pagination/pagination.html`` template, resulting in a
    Digg-like display of the available pages, given the current page.  If there
    are too many pages to be displayed before and after the current page, then
    elipses will be used to indicate the undisplayed gap between page numbers.

    Requires one argument, ``context``, which should be a dictionary-like data
    structure and must contain the following keys:

    ``paginator``
        A ``Paginator`` or ``QuerySetPaginator`` object.

    ``page_obj``
        This should be the result of calling the page method on the
        aforementioned ``Paginator`` or ``QuerySetPaginator`` object, given
        the current page.

    This same ``context`` dictionary-like data structure may also include:

    ``getvars``
        A dictionary of all of the **GET** parameters in the current request.
        This is useful to maintain certain types of state, even when requesting
        a different page.
        """
    try:
        paginator = context['paginator']
        page_obj = context['page_obj']
        page_range = paginator.page_range
        # First and last are simply the first *n* pages and the last *n* pages,
        # where *n* is the current window size.
        first = set(page_range[:window])
        last = set(page_range[-window:])
        # Now we look around our current page, making sure that we don't wrap
        # around.
        current_start = page_obj.number-1-window
        if current_start < 0:
            current_start = 0
        current_end = page_obj.number-1+window
        if current_end < 0:
            current_end = 0
        current = set(page_range[current_start:current_end])
        pages = []
        # If there's no overlap between the first set of pages and the current
        # set of pages, then there's a possible need for elusion.
        if len(first.intersection(current)) == 0:
            first_list = list(first)
            first_list.sort()
            second_list = list(current)
            second_list.sort()
            pages.extend(first_list)
            diff = second_list[0] - first_list[-1]
            # If there is a gap of two, between the last page of the first
            # set and the first page of the current set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            unioned = list(first.union(current))
            unioned.sort()
            pages.extend(unioned)
        # If there's no overlap between the current set of pages and the last
        # set of pages, then there's a possible need for elusion.
        if len(current.intersection(last)) == 0:
            second_list = list(last)
            second_list.sort()
            diff = second_list[0] - pages[-1]
            # If there is a gap of two, between the last page of the current
            # set and the first page of the last set, then we're missing a
            # page.
            if diff == 2:
                pages.append(second_list[0] - 1)
            # If the difference is just one, then there's nothing to be done,
            # as the pages need no elusion and are correct.
            elif diff == 1:
                pass
            # Otherwise, there's a bigger gap which needs to be signaled for
            # elusion, by pushing a None value to the page list.
            else:
                pages.append(None)
            pages.extend(second_list)
        else:
            differenced = list(last.difference(current))
            differenced.sort()
            pages.extend(differenced)
        to_return = {
            'pages': pages,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.count > paginator.per_page,
        }
        if 'request' in context:
            getvars = context['request'].GET.copy()
            if 'page' in getvars:
                del getvars['page']
            if len(getvars.keys()) > 0:
                to_return['getvars'] = "&%s" % getvars.urlencode()
            else:
                to_return['getvars'] = ''
        return to_return
    except KeyError, AttributeError:
        return {}

register.inclusion_tag('pagination/pagination.html', takes_context=True)(paginate)
