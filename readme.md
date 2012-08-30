# Day Z Log

Application to share and follow <a href="http://dayzmod.com">Day Z</a> stories on the web. Hacked together using a variety of Python/Django stuff.

## Todo

- Blog
    - jQuery/AJAX for voting (use http://vanilla-js.com/ :)
    - Previous/Next entry by user
    - Markdown preview with Markedit, imgur for image hosting
    - Comments with Disqus
- Relationship
    - Use <https://github.com/coleifer/django-relationships/> or <https://github.com/nathanborror/django-basic-apps/tree/master/basic/relationships>
- About / Help dedicated pages
    - Help <a href="http://community.bistudio.com/wiki/squad.xml">squad.xml</a>, finding player id, etc.
- Feeds & Content Export
        - Atom XML and JSON
- [Cacheing](https://docs.djangoproject.com/en/dev/topics/cache/) for homepage view
- Use South

### Future

- Profile image?
- In-game player logo via squad.xml?
- Vanity URLs
    - http://www.elfsternberg.com/2009/06/26/dynamic-names-as-first-level-url-path-objects-in-django/
    - http://stackoverflow.com/questions/3013098/django-username-in-url-instead-of-id
    - http://stackoverflow.com/questions/3333765/get-user-from-url-segment-with-django