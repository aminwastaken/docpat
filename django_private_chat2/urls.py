# -*- coding: utf-8 -*-
from django.urls import path, re_path
from . import consumers
from . import views

app_name = 'django_private_chat2'
websocket_urlpatterns = [
    re_path(r'^chat_ws$', consumers.ChatConsumer.as_asgi()),
]

urlpatterns = [
    path('messages/send/<int:dialog_with>', views.send_message, name='send_message'),
    path('messages/<int:dialog_with>/', views.MessagesModelList.as_view(), name='messages_list'),
    path('chat/', views.DialogsModelList.as_view(), name='dialogs_list'),

    # path('self/', views.SelfInfoView.as_view(), name='self_info'),
    # path('messages/', views.MessagesModelList.as_view(), name='all_messages_list'),
    # path('upload/', views.UploadView.as_view(), name='fileupload'),
]
