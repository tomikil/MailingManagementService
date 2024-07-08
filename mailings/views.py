from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogs.models import Blog
from clients.models import Client
from mailings.forms import MailingParametersForm, MailingParametersManagerForm, MessageForm
from mailings.models import MailingParameters, Message, Logs


class MailingParametersListView(LoginRequiredMixin, ListView):
    model = MailingParameters
    template_name = './mailings/mailingparameters_list.html'

    def get_queryset(self, qurester=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingParametersDetailsView(LoginRequiredMixin, DetailView):
    model = MailingParameters

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager') and user != self.object.owner:
            raise PermissionDenied
        else:
            return self.object


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

    def get_success_url(self):
        return reverse('mailings:detail', args=[self.kwargs.get('pk')])

    def get_form_class(self):
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return MailingParametersForm
        if user.has_perm('mailings.deactivate_mailing'):
            return MailingParametersManagerForm
        raise PermissionDenied


class MailingParametersDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingParameters
    success_url = reverse_lazy('mailings:list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_queryset(self, queryset=None):
        queryset = super().get_queryset()
        user = self.request.user
        if not user.is_superuser and not user.groups.filter(name='manager'):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


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

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('mailings:message_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.request.user == self.object.owner or self.request.user.is_superuser:
            return self.object
        raise PermissionDenied


class LogsListView(LoginRequiredMixin, ListView):
    model = Logs


def index(request):
    count_mailing_items = MailingParameters.objects.count()
    count_active_mailing_items = MailingParameters.objects.filter(status='is_active').count()
    count_unic_clients = Client.objects.values_list('email', flat=True).count()
    random_blogs = Blog.objects.order_by('?')[:3]
    context = {'count_mailing_items': count_mailing_items,
               'count_active_mailing_items': count_active_mailing_items,
               'count_unic_clients': count_unic_clients,
               'random_blogs': random_blogs,
               }

    return render(request, 'mailings/index.html', context)
