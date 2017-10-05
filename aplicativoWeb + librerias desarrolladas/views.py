from __future__ import division

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView

from .forms import AddProviderEdgeWithOUTClientForm, AddClientToProviderEdgeForm, AddProviderEdgeWithClientForm, CommunicateVrfsInProviderEdgesForm, ProviderEdgeViewForm, CustomerEdgeViewForm, SwitchViewForm, AddProviderForm

import funcionesGenerales as fg

import conexionSSH as cs

import scripts as s


class WelcomeView(TemplateView):
    template_name = 'welcome.html'

    def get_context_data(self, *args, **kwargs):
        context = super(WelcomeView, self).get_context_data(*args, **kwargs)
        return context

class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        return context

def CreateProviderView(request):
    title = "Create Provider!"
    form = AddProviderForm()
    salida = "inicializando variable 'salida' "
    if request.method=='POST':
        form = AddProviderForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            loopback = cd.get('loopback')
            print cd.get('loopback')
            s.initializeNewProvider(loopback)
    else:
        form = AddProviderForm()
    return render(request, "create-p.html",{
        'form': form,
        'title': title,
        'salida': salida
    })

class ProviderView(TemplateView):
    template_name = 'provider.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProviderView, self).get_context_data(*args, **kwargs)
        return context

def ShowMPLSLDPNeigborView(request):
    title = "Emitir comando show mpls ldp neighbor!"
    salida = "inicializando variable 'salida' "
    salida = cs.presentarShow("P1","show mpls ldp neighbor")
    initializeNewProvider()
    return render(request, "show-mpls-ldp-neighbor.html",{
        'title': title,
        'salida': salida
    })

def ProviderEdgeView(request):
    title = "Provider Edge!"
    form = ProviderEdgeViewForm()
    salida = "inicializando variable 'salida' "
    if request.method=='POST':
        form = ProviderEdgeViewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            equipo = cd.get('equipo')
            comando = cd.get('comando')
            nombrevrf = cd.get('nombrevrf')
            
            print equipo
            print comando
            print cd.get('nombrevrf')
            
            # Duty
            if comando == "show ip route vrf":
                
                # enviar comando
                salida = "salida == show ip route vrf"
                print salida
            else:
                # enviar comando
                salida = "salida != show ip route vrf"
                print salida
    else:
        form = ProviderEdgeViewForm()
    return render(request, "provider-edge.html",{
        'form': form,
        'title': title,
        'salida': salida
    })

def CustomerEdgeView(request):
    title = "Customer Edge!"
    form = CustomerEdgeViewForm()
    salida = "inicializando variable 'salida' "
    if request.method=='POST':
        form = CustomerEdgeViewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            equipo = cd.get('equipo')
            comando = cd.get('comando')
            
            print equipo
            print comando
            
            # Duty
            if comando == "ping vrf":
                nombre_vrf = cd.get('nombre_vrf')
                ip_destino = cd.get('ip_destino')
                print "nombre_vrf: " + str(nombre_vrf)
                print "ip_destino: " + str(ip_destino)
                # enviar comando
                salida = "salida == ping vrf"
                print salida
            else:
                # enviar comando
                salida = "salida != ping vrf"
                print salida
    else:
        form = CustomerEdgeViewForm()
    return render(request, "customer-edge.html",{
        'form': form,
        'title': title,
        'salida': salida
    })

def SwitchView(request):
    title = "Switch Edge!"
    form = SwitchViewForm()
    salida = "inicializando variable 'salida' "
    if request.method=='POST':
        form = SwitchViewForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            equipo = cd.get('equipo')
            print equipo
            
            # Duty
            salida = "salida == show vlan brief"
            print salida
            # enviar comando
    else:
        form = SwitchViewForm()
    return render(request, "switch.html",{
        'form': form,
        'title': title,
        'salida': salida
    })

def AddProviderEdgeWithoutClientView(request):
    title = "Add Provider Edge Without Client!"
    form = AddProviderEdgeWithOUTClientForm()
    if request.method=='POST':
        form = AddProviderEdgeWithOUTClientForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            provider_id = cd.get('provider_id')
            print provider_id
            fg.addProviderEdgeWithOUTClient(provider_id)
            return HttpResponseRedirect('/home/')
    else:
        form = AddProviderEdgeWithOUTClientForm()
    return render(request, "form-add-pe-without-client.html",{
        'form': form,
        'title': title
    })

def AddClientToProviderEdgeView(request):
    title = "Add Client to Provider Edge!"
    form = AddClientToProviderEdgeForm()
    if request.method=='POST':
        form = AddClientToProviderEdgeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            provider_edge_id = cd.get('provider_edge_id')
            nombre_cliente = cd.get('nombre_cliente')
            es_nuevo = cd.get('es_nuevo')
            print provider_edge_id
            print nombre_cliente
            print es_nuevo
            # Duty
            fg.addClientToProviderEdge(provider_edge_id,nombre_cliente,es_nuevo)
            return HttpResponseRedirect('/home/')
    else:
        form = AddClientToProviderEdgeForm()
    return render(request, "form-add-client-to-pe.html",{
        'form': form,
        'title': title
    })

def AddProviderEdgeWithClientView(request):
    title = "Add Provider Edge With Client!"
    form = AddProviderEdgeWithClientForm()
    if request.method=='POST':
        form = AddProviderEdgeWithClientForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            provider_id = cd.get('provider_id')
            nombre_cliente = cd.get('nombre_cliente')
            es_nuevo = cd.get('es_nuevo')
            print provider_id
            print nombre_cliente
            print es_nuevo
            # Duty
            fg.addProviderEdgeWithClient(provider_id,nombre_cliente,es_nuevo)
            return HttpResponseRedirect('/home/')
    else:
        form = AddProviderEdgeWithClientForm()
    return render(request, "form-add-pe-with-client.html",{
        'form': form,
        'title': title
    })

def CommunicateVrfsInProviderEdgesView(request):
    title = "Add Provider Edge With Client!"
    form = CommunicateVrfsInProviderEdgesForm()
    if request.method=='POST':
        form = CommunicateVrfsInProviderEdgesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            vrf_1 = cd.get('vrf_1')
            vrf_2 = cd.get('vrf_2')
            provider_edge_id_1 = cd.get('provider_edge_id_1')
            provider_edge_id_2 = cd.get('provider_edge_id_2')
            print vrf_1
            print vrf_2
            print provider_edge_id_1
            print provider_edge_id_2
            # Duty
            fg.ComunicateVrfsInProviderEdges(vrf_1,vrf_2,provider_edge_id_1,provider_edge_id_2)
            return HttpResponseRedirect('/home/')
    else:
        form = CommunicateVrfsInProviderEdgesForm()
    return render(request, "form-communicate-vrfs-in-pe.html",{
        'form': form,
        'title': title
    })