from urllib import request
from django import forms

from accounts.models import CustomUser

class MessageForm(forms.Form):
    message = forms.CharField(label='New Message')

class DialogForm(forms.Form):
    usernameList = CustomUser.objects.values_list('username')
    idList = CustomUser.objects.values_list('id')
    choicesList = idList.union(usernameList).order_by('username')

    userRecipient = forms.ChoiceField(choices=choicesList, label='List User')