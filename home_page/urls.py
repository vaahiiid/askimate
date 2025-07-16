from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('contact/', views.contact_form, name='contact_form'),
]
