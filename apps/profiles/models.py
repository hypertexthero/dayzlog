from django.db import models
from django.utils.translation import ugettext_lazy as _

from idios.models import ProfileBase

from datetime import datetime

# from imagekit.models.fields import ProcessedImageField
# from imagekit.models import ImageSpecField
# from imagekit.processors import ResizeToFill
from easy_thumbnails.fields import ThumbnailerImageField

class Profile(ProfileBase):
    name = models.CharField(_("In-Game Name"), max_length=50, null=True, blank=True, help_text="<b>Must match your Day Z in-game player name exactly <a href='/faq/#playername'>(what is my player name?)</a>. Required to make your profile information appear within Day Z.</b>")
    player_id = models.CharField(_("Player ID"), max_length=20, null=True, blank=True, help_text="<b>Must match your Day Z in-game player id exactly <a href='/faq/#playerid'>(what is my player id?)</a>. Required to make your profile information appear within Day Z.</b>")
    email = models.EmailField(_("Email"), blank=True, help_text="An email address you want other users to see, if any.")
    im = models.CharField(_("im"), max_length=50, null=True, blank=True, help_text="An instant messaging address you want other users to see, if any.")
    remark = models.TextField(_("remark"), null=True, blank=True, help_text="Any remarks you would like others to see.")
    player_img = models.ImageField(_("Image"), upload_to="player_img/%Y/%m/%d/", blank=True) # no player images yet
    # player_img = ProcessedImageField(_("Image"), upload_to="player_img/%Y/%m/%d/", blank=True) # no player images yet
    # player_thumb = ImageSpecField([ResizeToFill(260, 180)], format="JPEG", options={"quality": 75})
    date_joined = models.DateTimeField(_("Member Since"), default=datetime.now, editable=False)
    

# class ProfileForm(ModelForm):
#     class Meta:
#         model = Profile
#         # fields = ('name', 'player_id', 'email', 'im', 'remark',)
#         exclude = ("player_img", "email",)