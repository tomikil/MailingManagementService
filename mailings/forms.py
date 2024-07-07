from django.forms import ModelForm

from mailings.models import MailingParameters, Message


class MailingParametersForm(ModelForm):
    class Meta:
        model = MailingParameters
        exclude = ('owner', )


class MailingParametersManagerForm(ModelForm):
    class Meta:
        model = MailingParameters
        fields = ('status',)


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ('owner',)