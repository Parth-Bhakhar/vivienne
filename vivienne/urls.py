"""
URL configuration for vivienne project.

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
from django.contrib import admin
from django.urls import path
from main.views import *

urlpatterns = [
    path('', admin),
    path('admin/', admin),
    path('add_product/', add_product, name='add_product'),
    path('delete_product/', delete_product, name='delete_product'),
    path('update_product/', update_product, name='update_product'),
    path('view_product/', view_product, name='view_product'),
    path('update_rates/', update_rates, name='update_rates'),
    path('toggle-status/<int:product_id>/', toggle_product_status, name='toggle_product_status'),
    path('save_updated_data/', save_updated_data, name='save_updated_data'),
]
