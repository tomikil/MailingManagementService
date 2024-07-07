from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, UserListView, UserUpdateView

app_name = UsersConfig.name


urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    path('email_confirm/<str:token>', email_verification, name='email_confirm'),

    path('list/', UserListView.as_view(), name='list'),
    path('edit/<int:pk>/', UserUpdateView.as_view(), name='edit'),
]
