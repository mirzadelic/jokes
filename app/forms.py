from django import forms
from models import *


class JokeAdminForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(JokeAdminForm, self).__init__(*args, **kwargs)
        # set 'approved' to true when inserting new joke from admin panel
        self.fields['approved'].initial = True

    class Meta:
        model = Joke
        fields = ('text', 'category', 'approved', 'creator', 'email')
