from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('apply/', views.submit_application, name='submit_application'),
]
