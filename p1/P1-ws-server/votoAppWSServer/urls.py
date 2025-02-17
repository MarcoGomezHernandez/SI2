"""
URL configuration for VotingProj project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from votoAppWSServer.views import (CensoView, VotoView, ProcesoElectoralView)

urlpatterns = [
    # check if person is in "censo"
    path('censo/', CensoView.as_view(), name='censo'),
    # create "voto"
    path('voto/', VotoView.as_view(), name='voto'),
    # get list of "votos" associated with a given idProcesoElectoral
    path('procesoelectoral/<str:idProcesoElectoral>/', ProcesoElectoralView.as_view(), name='procesoelectoral'),
    # delete "voto" with id id_voto
    path('voto/<str:id_voto>/', VotoView.as_view(), name='voto'),
    ]
