"""
URL configuration for system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from logging import info
from django.contrib import admin
from django.urls import path
from application import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('phoneplan/', views.phoneplan, name='phoneplan'),
    path('payingpage/', views.payingpage, name='payingpage'),
    path('paymentmethod/', views.paymentmethod, name='paymentmethod'),
    path('confirmationpage/', views.confirmationpage, name='confirmationpage'),
    path('account_info/', views.account_info, name='account_info'),
    path('remove_plan/', views.remove_plan, name='remove_plan'),
    path('remove_payment_method/', views.remove_payment_method, name='remove_payment_method'),

]



