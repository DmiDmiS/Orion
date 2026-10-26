from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('apartment/<int:pk>/book/', views.book, name='book'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorite/<int:pk>/', views.favorite_toggle, name='favorite_toggle'),
    path('management/', views.management, name='management'),
    path('employees/', views.employees, name='employees'),
    path('requests/', views.requests_list, name='requests'),
    path('contract/new/<int:pk>/', views.contract_create, name='contract_create'),
    path('contracts/', views.contracts, name='contracts'),
    path('reports/', views.reports, name='reports'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
