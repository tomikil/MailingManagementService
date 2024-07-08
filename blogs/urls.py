from django.urls import path
from django.views.decorators.cache import cache_page

from blogs.apps import BlogsConfig
from blogs.views import (BlogCreateView, BlogListView, BlogDetailView, BlogUpdateView,
                         BlogDeleteView)

app_name = BlogsConfig.name

urlpatterns = [
    path('create/', BlogCreateView.as_view(), name='create'),
    path('', BlogListView.as_view(), name='list'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete'),
    path('edit/<int:pk>/', BlogUpdateView.as_view(), name='edit'),
    path('view/<int:pk>/', cache_page(60)(BlogDetailView.as_view()), name='view'),
]
