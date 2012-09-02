# Day Z Log

Application to share and follow <a href="http://dayzmod.com">Day Z</a> stories on the web. Made using a variety of Django applications and Twitter Bootstrap.

## Todo Before Launch

- About / Help dedicated pages
    - Help for [squad xml](http://community.bistudio.com/wiki/squad.xml, finding player id, adding Day Z Log URL to in-game profile, etc.
- Enable Comments with Disqus
- Setup South for DB migrations

## Future Features

- Blog
    - Markdown preview with Markedit, imgur for image hosting
    - jQuery/AJAX for voting (use http://vanilla-js.com/ :)
    - Previous/Next entry by user
    - Feeds & Content Export in Atom XML and JSON
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