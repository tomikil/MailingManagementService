from django.contrib import admin

from mailings.models import Message, MailingParameters, Logs


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')


@admin.register(MailingParameters)
class MailingParametersAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'message', 'start_date', 'end_date', 'next_date', 'interval', 'status')
    search_fields = ('client', 'status')
    list_filter = ('client', 'status')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_time_mailing', 'status_mailing', 'response', 'mailing_parameters')
