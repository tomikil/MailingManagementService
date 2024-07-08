from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from blogs.forms import BlogForm
from blogs.models import Blog
from blogs.services import get_articles_from_cache


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    form_class = BlogForm
    success_url = reverse_lazy('blogs:list')
    permission_required = 'blogs.add_blog'

    def form_valid(self, form):
        if form.is_valid():
            form.save()
        return super().form_valid(form)


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        queryset = get_articles_from_cache().filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.country += 1
        self.object.save()
        return self.object


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    permission_required = 'blogs.change_blog'

    def get_success_url(self):
        return reverse('blogs:detail', args=[self.kwargs.get('pk')])


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    success_url = reverse_lazy('blogs:list')
    permission_required = 'blogs.delete_blog'
