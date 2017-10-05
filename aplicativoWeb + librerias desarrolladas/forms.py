from django import forms

class AddProviderForm(forms.Form):
	loopback = forms.CharField(max_length=20)

class AddProviderEdgeWithOUTClientForm(forms.Form):
	provider_id = forms.CharField(max_length=20)

class AddClientToProviderEdgeForm(forms.Form):
	provider_edge_id 	= forms.CharField(max_length=20)
	nombre_cliente 		= forms.CharField(max_length=20)
	es_nuevo			= forms.BooleanField(required=False)

class AddProviderEdgeWithClientForm(forms.Form):
	provider_id 		= forms.CharField(max_length=20)
	nombre_cliente 		= forms.CharField(max_length=20)
	es_nuevo			= forms.BooleanField(required=False)

class CommunicateVrfsInProviderEdgesForm(forms.Form):
	vrf_1		 		= forms.CharField(max_length=20)
	vrf_2 				= forms.CharField(max_length=20)
	provider_edge_id_1 	= forms.CharField(max_length=20)
	provider_edge_id_2 	= forms.CharField(max_length=20)

class ProviderEdgeViewForm(forms.Form):
	DEVICE_CHOICES  = (
					    ("PE1", "PE1"),
					    ("PE2", "PE2")
					)
	COMMAND_CHOICES = (
					    ("show ip route vrf", "show ip route vrf"),
					    ("show ip vrf", "show ip vrf"),
					    ("show ip bgp vpnv4 all summary", "show ip bgp vpnv4 all summary")
					)
	equipo 				= forms.ChoiceField(choices=DEVICE_CHOICES)
	comando 			= forms.ChoiceField(choices=COMMAND_CHOICES)
	nombrevrf 			= forms.CharField(max_length=20, required=False)

	def clean_nombre_vrf(self):
		comando 	= self.cleaned_data['comando']
		nombre_vrf 	= self.cleaned_data['nombrevrf']
		if comando == "show ip route vrf" and not nombre_vrf:
			raise forms.ValidationError(" El campo 'nombrevrf' es obligatorio!")

class CustomerEdgeViewForm(forms.Form):
	DEVICE_CHOICES  = (
					    ("CE_TROPIBURGER_1", "CE_TROPIBURGER_1")
					)
	COMMAND_CHOICES = (
					    ("show ip route", "show ip route"),
					    ("show ip interface brief", "show ip interface brief")
					)
	equipo 				= forms.ChoiceField(choices=DEVICE_CHOICES)
	comando 			= forms.ChoiceField(choices=COMMAND_CHOICES)
	nombre_vrf 			= forms.CharField(max_length=20, required=False)
	ip_destino			= forms.CharField(max_length=20, required=False)

	def clean_nombre_vrf_ip_destino(self):
		comando 	= self.cleaned_data['comando']
		nombre_vrf 	= self.cleaned_data['nombre_vrf']
		ip_destino 	= self.cleaned_data['ip_destino']
		if comando == "show ip route vrf" and nombre_vrf=="" and ip_destino=="":
			raise forms.ValidationError("Los campos 'nombre_vrf' y 'ip_destino' son obligatorios!")

class SwitchViewForm(forms.Form):
	DEVICE_CHOICES  = (
					    ("PE1", "PE1"),
					    ("PE2", "PE2")
					)
	equipo 				= forms.ChoiceField(choices=DEVICE_CHOICES)