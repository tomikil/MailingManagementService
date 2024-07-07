from django.forms import ModelForm

from clients.models import Client


class ClientForm(ModelForm):
    class Meta:
        model = Client
        exclude = ('owner',)
