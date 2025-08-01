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
    path('answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619', views.POSTanswers),
    path('statistics_26a73614cf8dd8f7aeffec47fef1b6201896ece31e52a0c706ad5b7513f7851a', views.GETstatistics),
    path('check_people_0bb97721ff2c77036c66e6953a6ea632a424e36e6730fe74df52e3bbe6fcfa66', views.GETcheckPeople),
]
