"""muypicky URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView

from restaurants.views import  HomeView, WelcomeView, ProviderView, ProviderEdgeView, CustomerEdgeView, SwitchView, AddProviderEdgeWithoutClientView, AddClientToProviderEdgeView, AddProviderEdgeWithClientView, CommunicateVrfsInProviderEdgesView, ShowMPLSLDPNeigborView, CreateProviderView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^welcome/$', WelcomeView.as_view(), name='welcome'),
    
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contact.html')),

    url(r'^create-p/$', CreateProviderView, name="create-p"),    
    
    url(r'^provider/$', ProviderView.as_view(), name='provider'),
    url(r'^show-mpls-ldp-neighbor/$', ShowMPLSLDPNeigborView, name='show-mpls-ldp-neighbor'),

    url(r'^provider-edge/$', ProviderEdgeView, name='provider-edge'),
    url(r'^customer-edge/$', CustomerEdgeView, name='customer-edge'),
    url(r'^switch/$', SwitchView, name='switch'),

    url(r'^add-pe-without-client/$', AddProviderEdgeWithoutClientView, name='add-pe-without-client'),
    url(r'^add-client-to-pe/$', AddClientToProviderEdgeView, name='add-client-to-pe'),
    url(r'^add-pe-with-client/$', AddProviderEdgeWithClientView, name='add-pe-with-client'),
    url(r'^communicate-vrfs-in-pe/$', CommunicateVrfsInProviderEdgesView, name='communicate-vrfs-in-pe'),#
]
