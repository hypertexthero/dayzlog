from django import forms
from django.forms import ModelForm
import datetime

from models import Note
from widgets import SplitSelectDateTimeWidget
import settings

# Using ModelForm here to override the model's default text input widget and have a drop down menu with selectable date and time. Also needed to specify form_class=NoteForm in the create_object and update_object generic views functions in views.py

class NoteForm(ModelForm): 
    created = forms.DateTimeField(
        widget = SplitSelectDateTimeWidget(
            years=range(1978, datetime.datetime.now().year+10) # The years argument was necessary to specify a range of selectable years so an article can be set to be published automatically in a future date - http://stackoverflow.com/questions/3232364/display-a-series-of-dropdown-lists-with-past-dates-in-django
            ), 
        # finally fixed bug where current time to the second was not being called with the help of http://stackoverflow.com/a/2771701/412329
        # datetime.now() was being evaluated when the model was defined, and not each time I added a record.
        # changed:
        # initial = datetime.datetime.now()
        # to:
        initial = datetime.datetime.now
    )
    # modified = forms.DateTimeField(widget=SplitSelectDateTimeWidget(twelve_hr=False)) 
    class Meta:
        model = Note 