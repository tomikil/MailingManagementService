from django.urls import path, include
from mailings.apps import MailingsConfig
from mailings.views import (MailingParametersListView, MailingParametersCreateView, MailingParametersDetailsView,
                            MailingParametersDeleteView, MailingParametersUpdateView, MessageListView,
                            MessageCreateView,
                            MessageUpdateView, MessageDeleteView, LogsListView)

app_name = MailingsConfig.name

urlpatterns = [
    path('', MailingParametersListView.as_view(), name='list'),
    path('create/', MailingParametersCreateView.as_view(), name='create'),
    path('detail/<int:pk>', MailingParametersDetailsView.as_view(), name='detail'),
    path('update/<int:pk>', MailingParametersUpdateView.as_view(), name='update'),
    path('delete/<int:pk>', MailingParametersDeleteView.as_view(), name='delete'),

    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>', MessageUpdateView.as_view(), name='message_update'),
    path('message_delete/<int:pk>', MessageDeleteView.as_view(), name='message_delete'),

    path('logs_list/', LogsListView.as_view(), name='logs_list'),
]
