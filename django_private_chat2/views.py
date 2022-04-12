# -*- coding: utf-8 -*-
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
    ListView,

)
from accounts.models import CustomUser

from django_private_chat2.forms import MessageForm

from .models import (
    MessageModel,
    DialogsModel,
    UploadedFile
)
from .serializers import serialize_message_model, serialize_dialog_model, serialize_file_model
from django.db.models import Q

from django.contrib.auth.mixins import LoginRequiredMixin

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.paginator import Page, Paginator
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser
from django.urls import reverse_lazy, reverse
from django.forms import ModelForm
import json

from django.shortcuts import render

def send_message(request, dialog_with):

    senderUser = CustomUser.objects.get(id=request.user.pk)
    recipientUser = CustomUser.objects.get(id=dialog_with)
    
    newMessage = MessageModel(sender=senderUser, recipient=recipientUser, text=request.POST['message'])
    newMessage.save()

    return HttpResponseRedirect(reverse('django_private_chat2:messages_list', args=(dialog_with,)))

def create_dialog(request):

    senderUser = CustomUser.objects.get(id=request.user.pk)
    recipientUser = CustomUser.objects.get(id=request.POST['userRecipient'])

    try:
        newDialog = DialogsModel(user1=senderUser, user2=recipientUser)
        newDialog.save()
    except :
        return HttpResponseRedirect(reverse('django_private_chat2:dialogs_list'))


    return HttpResponseRedirect(reverse('django_private_chat2:dialogs_list'))

class MessagesModelList(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'MESSAGES_PAGINATION', 500)

    def get_queryset(self):
        if self.kwargs.get('dialog_with'):
            qs = MessageModel.objects \
                .filter(Q(recipient=self.request.user, sender=self.kwargs['dialog_with']) |
                        Q(sender=self.request.user, recipient=self.kwargs['dialog_with'])) \
                .select_related('sender', 'recipient')
        else:
            qs = MessageModel.objects.filter(Q(recipient=self.request.user) |
                                             Q(sender=self.request.user)).prefetch_related('sender', 'recipient', 'file')

        return qs.order_by('created')

    def render_to_response(self, context, **response_kwargs):

        user_pk = self.request.user.pk
        dialog_with = self.kwargs.get('dialog_with')
        form = MessageForm()
        data = [serialize_message_model(i, user_pk) for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')
        return_data = {
            'page': page.number,
            'pages': paginator.num_pages,
            'data': data,
            'form' : form,
            'dialog_with' : dialog_with
        }
        return render(self.request, 'django_private_chat2/chat.html', return_data)
        # return JsonResponse(return_data, **response_kwargs)


class DialogsModelList(LoginRequiredMixin, ListView):
    http_method_names = ['get', ]
    paginate_by = getattr(settings, 'DIALOGS_PAGINATION', 20)

    def get_queryset(self):
        qs = DialogsModel.objects.filter(Q(user1_id=self.request.user.pk) | Q(user2_id=self.request.user.pk)) \
            .select_related('user1', 'user2')
        return qs.order_by('-created')

    def render_to_response(self, context, **response_kwargs):
        user_pk = self.request.user.pk
        data = [serialize_dialog_model(i, user_pk) for i in context['object_list']]
        page: Page = context.pop('page_obj')
        paginator: Paginator = context.pop('paginator')

        usernameList = CustomUser.objects.values_list('username').exclude(id=self.request.user.pk)
        idList = CustomUser.objects.values_list('id').exclude(id=self.request.user.pk)
        choicesList = idList.union(usernameList).order_by('username')

        return_data = {
            'page': page.number,
            'pages': paginator.num_pages,
            'data': data,
            'choicesList': choicesList
        }
        return render(self.request, 'django_private_chat2/listUser.html', return_data)


class SelfInfoView(LoginRequiredMixin, DetailView):
    def get_object(self, queryset=None):
        return self.request.user

    def render_to_response(self, context, **response_kwargs):
        user: AbstractBaseUser = context['object']
        data = {
            "username": user.get_username(),
            "pk": str(user.pk)
        }
        return render(self.request, 'django_private_chat2/self.html', data)
        # return JsonResponse(data, **response_kwargs)


# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
# MAX_UPLOAD_SIZE = getattr(settings, 'MAX_FILE_UPLOAD_SIZE', 5242880)

class UploadForm(ModelForm):
    # TODO: max file size validation
    # def check_file(self):
    #     content = self.cleaned_data["file"]
    #     content_type = content.content_type.split('/')[0]
    #     if (content._size > MAX_UPLOAD_SIZE):
    #         raise forms.ValidationError(_("Please keep file size under %s. Current file size %s")%(filesizeformat(MAX_UPLOAD_SIZE), filesizeformat(content._size)))
    #     return content
    #
    # def clean(self):

    class Meta:
        model = UploadedFile
        fields = ['file']


class UploadView(LoginRequiredMixin, CreateView):
    http_method_names = ['post', ]
    model = UploadedFile
    form_class = UploadForm

    def form_valid(self, form: UploadForm):
        self.object = UploadedFile.objects.create(uploaded_by=self.request.user, file=form.cleaned_data['file'])
        return JsonResponse(serialize_file_model(self.object))

    def form_invalid(self, form: UploadForm):
        context = self.get_context_data(form=form)
        errors_json: str = context['form'].errors.get_json_data()
        return HttpResponseBadRequest(content=json.dumps({'errors': errors_json}))
