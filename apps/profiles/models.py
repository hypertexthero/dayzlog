from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase


class Profile(ProfileBase):
    # name = models.CharField(_("name"), max_length=50, null=True, blank=True, help_text="Make sure this matches your Day Z in-game profile username exactly.")
    # about = models.TextField(_("about"), null=True, blank=True) # remark?
    # location = models.CharField(_("location"), max_length=40, null=True, blank=True)
    # website = models.URLField(_("website"), null=True, blank=True, verify_exists=False)

    # =todo: fields matching day z player profile
    name = models.CharField(_("In-Game Name"), max_length=50, null=True, blank=True, help_text="<b>Must match your Day Z in-game profile name exactly</b> <a data-toggle='modal' href='#help'>(what is my profile name?)</a>. Required to make your profile information appear within Day Z.")
    player_id = models.CharField(_("Player ID"), max_length=20, null=True, blank=True, help_text="<b>Must match your Day Z in-game profile player id exactly</b> <a data-toggle='modal' href='#help'>(what is my player id?)</a>. Required to make your profile information appear within Day Z.")
    email = models.EmailField(blank=True, verbose_name='Email', help_text="An email address you want other users to see, if any.")
    im = models.CharField(_("im"), max_length=50, null=True, blank=True, help_text="An instant messaging address you want other users to see, if any.")
    remark = models.TextField(_("remark"), null=True, blank=True, help_text="Any remarks you would like others to see.")



# http://stackoverflow.com/questions/1910359/creating-a-extended-user-profile
# from django.contrib.auth.models import User
# from django.db.models.signals import post_save
# def create_blog(sender, **kw):
#     user = kw["instance"]
#     slug = kw["user"]
#     if kw["created"]:
#         up = Profile(user=user, slug=slug, description=description)
#         up.save()
# post_save.connect(create_blog, sender=User)

# from django.db.models.signals import post_save # http://stackoverflow.com/a/965883/412329
# from django.dispatch import receiver # https://docs.djangoproject.com/en/dev/topics/signals/#receiver-functions
# # add users who register using front-end form to the 'contributors' group automatically
# # http://stackoverflow.com/a/8949526/412329
# # =todo: try this alternative: http://sontek.net/extending-the-django-user-model
# @receiver(post_save, sender=User, dispatch_uid='accounts.models.user_post_save_handler')
# def user_post_save(sender, instance, created, **kwargs):
#     """ This method is executed whenever an user object is saved - automatically adding users who register using the front-end form to the 'contributors' group                                  
#     """
#     if created:
#         instance.groups.add(Group.objects.get(name='contributors'))