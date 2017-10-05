import paramiko




# FUNCION QUE ENVIA UN COMANDO Y RETORNA SU STDOUT 
def enviar_comando_para_show(ip, comando, usuario, contrasena):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(ip, port=22, username=usuario, password=contrasena)
	stdin, stdout, stderr = ssh.exec_command(comando)
	time.sleep(2)
	output =stdout.readlines()
	type(output)
	return '\n'.join(output)




# PROVIDER
def show_mpls_ldp_neigbor():
	# Como solo hay un provider, lo dejamos fijo
	ip 			= ''
	comando 	= 'show mpls ldp neighbor'
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)




# PROVIDER EDGE
def show_ip_route_vrf(ip, nombre_vrf):
	comando 	= 'show ip route vrf ' + nombre_vrf
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)

def show_ip_vrf(ip):
	comando 	= 'show ip vrf'
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)

def show_ip_bgp_vpnv4_all_summary(ip):
	comando 	= 'show ip bgp vpnv4 all summary'
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)




# CUSTOMER EDGE

def show_ip_route(ip):
	comando 	= 'show ip route'
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)

def ping_vrf(ip, nombre_vrf, ip_destino):
	comando 	= 'ping vrf ' + nombre_vrf + ' ' + ip_destino
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)




# SWITCH
def show_vlan_brief(ip):
	comando 	= 'show vlan brief'
	usuario 	= 'admin'
	contrasena 	= 'admin'
	return enviar_comando_para_show(ip, comando, usuario, contrasena)










