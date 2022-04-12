from urllib import request
from django import forms


class MessageForm(forms.Form):
    message = forms.CharField(label='New Message')