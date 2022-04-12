from cProfile import label
from email import message
from logging import PlaceHolder
from django import forms

class MessageForm(forms.Form):
    message = forms.CharField(label='message')