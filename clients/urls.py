
from django.urls import path, include
from clients.apps import ClientsConfig
from clients.views import ClientListView, ClientCreateView, ClientDetailView, ClientUpdateView, ClientDeleteView

app_name = ClientsConfig.name

urlpatterns = [
    path('list/', ClientListView.as_view(), name='list'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('detail/<int:pk>/', ClientDetailView.as_view(), name='detail'),
    path('update/<int:pk>/', ClientUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='delete'),
]
