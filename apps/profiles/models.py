from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase

# from django import forms
# from django.forms import ModelForm

class Profile(ProfileBase):
    name = models.CharField(_("In-Game Name"), max_length=50, null=True, blank=True, help_text="<b>Must match your Day Z in-game profile name exactly</b> <a data-toggle='modal' href='#help'>(what is my profile name?)</a>. Required to make your profile information appear within Day Z.")
    player_id = models.CharField(_("Player ID"), max_length=20, null=True, blank=True, help_text="<b>Must match your Day Z in-game profile player id exactly</b> <a data-toggle='modal' href='#help'>(what is my player id?)</a>. Required to make your profile information appear within Day Z.")
    email = models.EmailField(blank=True, verbose_name="Email", help_text="An email address you want other users to see, if any.")
    im = models.CharField(_("im"), max_length=50, null=True, blank=True, help_text="An instant messaging address you want other users to see, if any.")
    remark = models.TextField(_("remark"), null=True, blank=True, help_text="Any remarks you would like others to see.")
    player_img = models.ImageField(verbose_name="Image", upload_to="player_img/%Y/%m/%d/", blank=True) # no player images yet

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         # fields = ('name', 'player_id', 'email', 'im', 'remark',)
#         exclude = ("player_img", "email",)