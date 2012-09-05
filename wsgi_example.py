#!/usr/bin/python
# https://www.zoe.vc/2010/django-with-virtualenv-on-webfaction/ 
import os, sys, site
 
# add virtualenv python libs
site.addsitedir('/home/<yourusername>/webapps/<yourappname>/<yourvirtualenvname>/lib/python2.7/site-packages')
 
# append the project path to system path
sys.path.append('/home/<yourusername>/webapps/<yourappname>/<yourvirtualenvname>/')
sys.path.append('/home/<yourusername>/webapps/<yourappname>/<yourvirtualenvname>/<yourprojectname>')
 
# set the settings module
os.environ['DJANGO_SETTINGS_MODULE'] = '<yourprojectname>.settings'
 
# init the wsgi handler
# from django.core.handlers.wsgi import WSGIHandler
# application = WSGIHandler()

from django.core.handlers.wsgi import WSGIHandler
import pinax.env
# setup the environment for Django and Pinax
pinax.env.setup_environ(__file__)
# set application for WSGI processing
application = WSGIHandler()