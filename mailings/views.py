from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailings.forms import MailingParametersForm, MailingParametersManagerForm, MessageForm
from mailings.models import MailingParameters, Message, Logs


class MailingParametersListView(LoginRequiredMixin, ListView):
    model = MailingParameters
    template_name = './mailings/mailingparameters_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingParametersDetailsView(LoginRequiredMixin, DetailView):
    model = MailingParameters


class MailingParametersCreateView(LoginRequiredMixin, CreateView):
    model = MailingParameters
    form_class = MailingParametersForm
    success_url = reverse_lazy('mailings:list')

    def form_valid(self, form):
        mailing = form.save()
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingParametersUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingParameters
    form_class = MailingParametersForm
    success_url = reverse_lazy('mailings:list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner:
            return MailingParametersForm
        if user.has_perm('mailing.change_status'):
            return MailingParametersManagerForm
        raise PermissionDenied


class MailingParametersDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingParameters
    success_url = reverse_lazy('mailings:list')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:create')

    def form_valid(self, form):
        message = form.save()
        message.sender = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailings:message_list')


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs


