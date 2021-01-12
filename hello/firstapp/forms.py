from django import forms

PERIOD_CHOICES = (
    ("7day", "7day"),
    ("1month", "1month"),
    ("3month", "3month"),
    ("6month", "6month"),
    ("12month", "12month"),
    ("overall", "overall"),
)


class ArtistForm(forms.Form):
    name = forms.CharField(label="Artist")


class UserNameForm(forms.Form):
    username = forms.CharField(label="User", required=False)


class PeriodForm(forms.Form):
    period = forms.ChoiceField(choices=PERIOD_CHOICES)
