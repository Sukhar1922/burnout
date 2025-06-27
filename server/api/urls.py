"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.test),
    path('questions_368c231b7c9a3d506cef5a936c83d92f068179d849db19ac2608ba288c7c1c56', views.GETquestions),
    path('fill_table_808b0abd590b48de048dfef7abadcd06410a24c9f9619a05aef83a9eb30ad765', views.fillQuestions),
    path('registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d', views.POSTregistration),
]
