from django.urls import path

from . import views

app_name = 'item'

urlpatterns = [
    path('', views.items, name='items'),
    path('new/', views.new, name='new'),
    path('<int:item_id>/', views.detail, name='detail'),
    path('delete/<int:item_id>/', views.delete, name='delete'),
    path('edit/<int:item_id>/', views.edit, name='edit'),
]