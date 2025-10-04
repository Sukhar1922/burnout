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
    path('registration_8d6238094a7742ac22fedb3a180bc590d35f5ea70b8a262cc0bd976349b6181d', views.POSTregistration),
    path('check_nickname_4b4f04bfd927c2a6381a392dcfedcd258e7dfb6e0401f674b13bc4c0db01bcb5', views.GETcheckNickname),
    path('answers_d4266fadaf6b4d8d557160643324a1d9470a5dc0ad973784f553b6918fc4a619', views.POSTanswers),
    path('statistics_26a73614cf8dd8f7aeffec47fef1b6201896ece31e52a0c706ad5b7513f7851a', views.GETstatistics),
    path('check_people_0bb97721ff2c77036c66e6953a6ea632a424e36e6730fe74df52e3bbe6fcfa66', views.GETcheckPeople),
    path('everyweek_tasks_4a73556cb2e8ca050437f3868dccef0cee3bb02b5beb1b8d46882a43e452522e', views.EvereweekTasks),
    # path('test_tg', views.TestTG),
    path('options_33eafc9c4333dc5ecbe984d3b75cc9a683a3f86f143bb5ed68607947f5c20a19', views.OptionsAPI),
    path('everyday_answers_7f5831436bc60af14dd1d0c9a4d09f73092a2560d9d1e6d28eba22e6d9effce8', views.sendEveryDayAnswers),
    path('statistics_everyday_answers_c23820a3029e86a952fb596d5ac69ec7f5306625732ada45b7c09f926237728a', views.GETeverydayStatistics),
    path('statistics_everyweek_answers_ecc64aa6711cc716673a5a0dee90cb1ab9c5f5ac032087b50ef96b8ce12a05e9', views.GETeveryweekStatistics),
]
