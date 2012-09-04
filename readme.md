# Day Z Log

Application to share and follow <a href="http://dayzmod.com">Day Z</a> stories on the web. Made using a variety of Django applications and Twitter Bootstrap.

## Todo Before Launch

- Insert player roster screenshot in FAQ
- Setup [auto database backup](http://docs.webfaction.com/user-guide/databases.html#id2)
- Fix on production server (or ideally use vagrant to make production server exactly the same as development server - CentOS):
    - DatabaseError: value too long for type character varying(50)
    - TemplateSyntaxError: Couldn't get the thumbnail player_img/2012/09/04/Screen_Shot_2012-09-04_at_09.34.40.png: The source file does not appear to be an image
- Don't use virtualenv on production, instead get pip to install in the [webapp lib folder](http://forum.webfaction.com/viewtopic.php?pid=18258#p18258): 

    pip install my_package --install-option="--install-dir=$HOME/webapps/app_name/lib/python2.6" --install-option="--script-dir=$HOME/webapps/app_name/bin"

## Future Features

- Blog
    - Markdown preview with Markedit, imgur for image hosting
    - jQuery/AJAX for voting (use http://vanilla-js.com/ :)
    - Previous/Next entry by user
    - Feeds & Content Export in Atom XML and JSON
    - [Player image upload size/dimensions optimization](https://github.com/jdriscoll/django-imagekit)
        - <http://blog.bixly.com/post/4315807876/django-imagekit>
        - <http://stackoverflow.com/questions/2845000/resizing-image-on-upload-with-django-imagekit>
        - or <http://code.google.com/p/django-stdimage/>
- I18N, German & Russian to begin with
- [Cacheing](https://docs.djangoproject.com/en/dev/topics/cache/) for homepage view
- Profile images?
- Ability to close own account
- Profile list with alphabetical navigation
- In-game player logo via squad.xml?
- Vanity URLs?
    - http://www.elfsternberg.com/2009/06/26/dynamic-names-as-first-level-url-path-objects-in-django/
    - http://stackoverflow.com/questions/3013098/django-username-in-url-instead-of-id
    - http://stackoverflow.com/questions/3333765/get-user-from-url-segment-with-django