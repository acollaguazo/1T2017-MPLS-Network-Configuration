import ConsultasArchivos as CA

def getLoopbackFromNumber(loopbackNumber):
    return str(loopbackNumber) + "." + str(loopbackNumber) + "." + str(loopbackNumber) + "." + str(loopbackNumber)

"""
Esta funcion inicia el Provider sin entrar en configuracion de
ninguna de sus interfaces.
Solo configura Loopback y la red grande 192.168.0.0/16 en el network
de OSPF
"""
def initializeNewProvider(loopbackNumber):
    loopback = getLoopbackFromNumber(loopbackNumber)
    texto  = "end\n" \
             "conf t\n" \
             "hostname P"+str(loopbackNumber)+"\n" \
             "interface Loopback0\n" \
             "ip address NUEVALOOPBACKDELPROVIDER 255.255.255.255\n" \
             "router ospf 1\n" \
             "network NUEVALOOPBACKDELPROVIDER 0.0.0.0 area 0\n" \
             "network 192.168.0.0 0.0.255.255 area 0\n" \
             "exit\n" \
             "ip cef\n" \
             "mpls label protocol ldp\n" \
             "mpls ldp router-id Loopback0\n" \
             "mpls ip\n" \
             "do wr\n" \
             "\n"
    codigo = texto.replace("NUEVALOOPBACKDELPROVIDER",loopback)
    return codigo

def getIpForProviderInterface(ProviderEdgeNumber,ProviderNumber):
    return "192.168."+str(ProviderEdgeNumber)+str(ProviderNumber)+".1"

"""
Esta funcion realiza el inicio de una interface fisica del proveedor
con su ip. Esta ip no es necesaria de agregar al ospf pues en la
inicializacion de provider se puso toda la red 192.168.0.0/16 que
englobara las redes PE-P
"""
def newInterfaceForProvider(interfaceNueva,ProviderEdgeNumber,ProviderNumber):
    ipForProviderInterface = getIpForProviderInterface(ProviderEdgeNumber,ProviderNumber)
    texto  = "end\n" \
              "conf t\n" \
              "interface FastEthernet NUEVAINTERFACE/0\n" \
              "ip address NUEVOADDRESSDELAINTERFACE 255.255.255.252\n" \
              "mpls ip\n" \
              "no  shutdown\n" \
              "exit\n" \
              "do wr\n" \
              "\n"
    codigo = texto.replace("NUEVAINTERFACE",str(interfaceNueva)).replace("NUEVOADDRESSDELAINTERFACE", str(ipForProviderInterface))
    return codigo

def providerEdgesUpgradeForNewProviderEdge(loopbackNumber):
    loopback = getLoopbackFromNumber(loopbackNumber)
    texto = "end\n" \
            "conf t\n" \
            "router bgp 1\n" \
            "neighbor NUEVALOOPBACK remote-as 1\n" \
            "neighbor NUEVALOOPBACK update-source Loopback0\n" \
            "neighbor NUEVALOOPBACK next-hop-self\n" \
            "address-family vpnv4\n" \
            "neighbor NUEVALOOPBACK activate\n" \
            "neighbor NUEVALOOPBACK send-community extended\n" \
            "exit-address-family\n" \
            "exit\n" \
            "do wr\n" \
            "\n"
    codigo = texto.replace("NUEVALOOPBACK",loopback)
    return codigo

def getIpForProviderEdgeInterface(ProviderEdgeNumber,ProviderNumber):
    return "192.168."+str(ProviderEdgeNumber)+str(ProviderNumber)+".2"

def getIpNetForProviderEdgeInterface(ProviderEdgeNumber,ProviderNumber):
    return "192.168."+str(ProviderEdgeNumber)+str(ProviderNumber)+".0"

#Recordar Enviar en loopbackNumber el actual looback -1
def BGPInicio(loopbackNumber):
    texto = ""
    for Number in range(11,loopbackNumber):
        loopback = getLoopbackFromNumber(Number)
        texto+="neighbor NUEVOLOOPBACK remote-as 1\n" \
               "neighbor NUEVOLOOPBACK update-source Loopback0\n" \
               "neighbor NUEVOLOOPBACK next-hop-self\n\n".replace("NUEVOLOOPBACK",loopback)
    return texto

#Recordar Enviar en loopbackNumber el actual looback -1
def BGPInicio2(loopbackNumber):
    texto = ""
    for Number in range(11,loopbackNumber):
        loopback = getLoopbackFromNumber(Number)
        texto+="" \
               "neighbor NUEVOLOOPBACK activate\n" \
               "neighbor NUEVOLOOPBACK send-community extended\n".replace("NUEVOLOOPBACK",loopback)
    return texto

"""
Esta funcion inicializa un nuevo Provider Edge. No crea los clientes o las VRFS.
Esta funcion se encarga de:
    dar el respectivo IP address a la interface FastEthernet 0/0 que conecta con el Provider
    dar el respectivo IP address a la interface FastEthernet 1/0 que conecta con los Clientes
    Configuraciones OSPF, MPLS, BGP necesarias.
"""
def inicializeProviderEdge(loopbackNumber,ProviderNumber):
    texto="end\n" \
          "conf t\n" \
          "hostname PE"+str(loopbackNumber)+"\n" \
          "interface Loopback0\n" \
          "ip address NUEVALOOPBACK 255.255.255.255\n" \
          "interface FastEthernet0/0\n" \
          "ip address NUEVAIPADDRESS 255.255.255.252\n" \
          "mpls ip\n" \
          "no shutdown\n" \
          "interface FastEthernet1/0\n" \
          "no shutdown\n" \
          "exit\n"
    loopback = getLoopbackFromNumber(loopbackNumber)
    ipAddress = getIpForProviderEdgeInterface(loopbackNumber,ProviderNumber)
    Inicio = texto.replace("NUEVALOOPBACK",loopback).replace("NUEVAIPADDRESS",ipAddress)

    ConfiguracionOSPF = "" \
          "router ospf 1\n" \
          "network NUEVALOOPBACK 0.0.0.0 area 0\n" \
          "network NUEVAIPADDRESSRED 0.0.0.3 area 0\n" \
          "exit\n"
    ipNet = getIpNetForProviderEdgeInterface(loopbackNumber,ProviderNumber)
    ConfiguracionOSPF = ConfiguracionOSPF.replace("NUEVALOOPBACK",loopback).replace("NUEVAIPADDRESSRED",ipNet)

    ConfiguracionesBGP="" \
          "router bgp 1\n" \
          ""+BGPInicio(loopbackNumber)+"\n" \
          "no auto-summary\n" \
          "exit\n" \

    ConfiguracionesVarias="" \
          "ip cef\n" \
          "mpls label protocol ldp\n" \
          "mpls ldp router-id Loopback0\n" \
          "mpls ip\n" \

    ConfiguracionesBGP2="" \
          "router bgp 1\n" \
          "address-family vpnv4\n" \
          ""+BGPInicio2(loopbackNumber)+"\n" \
          "exit-address-family\n" \
          "exit\n"

    configuracionesVRF = ""


    CA.upgradeDispositiveDataBase("PE"+str(loopbackNumber),str(ipAddress))
    return Inicio+ConfiguracionOSPF+ConfiguracionesBGP+ConfiguracionesVarias+ConfiguracionesBGP2

def getIpForVrfInProviderEdge(ProviderEdgeNumber,subinterface):
    return "10."+str(ProviderEdgeNumber)+"."+str(subinterface)+"."+"1"

"""
La subinterface y la vlan de las VRFS deberan tener el mismo numero.
Crea la VRF para el cliente en el Provider Edge
Realiza las configuraciones necesarios en RIP y BGP para que los clientes sean reconocidos
"""
def insertVrfIntoProviderEdge(vrfName,subinterface,ProviderEdgeNumber):
    ipVRF = getIpForVrfInProviderEdge(ProviderEdgeNumber,subinterface)
    texto="end\n" \
          "conf t\n" \
          "ip vrf NOMBREVRF \n" \
          "rd 65535:SUB \n" \
          "route-target export SUB:SUB \n" \
          "route-target import SUB:SUB \n" \
          "interface FastEthernet1/0.SUB \n" \
          "encapsulation dot1Q SUB \n" \
          "ip vrf forwarding NOMBREVRF \n" \
          "ip address IPADDRESPARAVRF 255.255.255.0\n" \
          "no shutdown\n" \
          "exit\n" \
          "router rip\n" \
          "version 2\n" \
          "address-family ipv4 vrf NOMBREVRF \n" \
          "network 10."+str(ProviderEdgeNumber)+"."+str(subinterface)+".0\n" \
          "redistribute bgp 1 metric transparent\n" \
          "exit-address-family\n" \
          "no auto-summary\n" \
          "exit\n" \
          "router bgp 1\n" \
          "address-family ipv4 vrf NOMBREVRF\n" \
          "redistribute rip\n" \
          "exit-address-family\n" \
          "exit\n" \
          "do wr\n" \
          "\n"
    return texto.replace("NOMBREVRF",str(vrfName)).replace("SUB",str(subinterface)).replace("IPADDRESPARAVRF",ipVRF)

def getIpForVrfInClientEdge(ProviderEdgeNumber,subinterface,nombreCliente):
    file = open("archivos/Red_PE_Clientes.txt","r")
    ultimoOctetoUsado = 1
    for linea in file:
        if(linea!="\n"):
            (PEN,x,Sub,octeto) = linea.strip().split(",")
            if(int(ProviderEdgeNumber)==int(PEN) and int(Sub)==int(subinterface)):
                if(int(ultimoOctetoUsado)<int(octeto)):
                    ultimoOctetoUsado=int(octeto)
    #considerar que esta funcion se usa solo para generar el codigo... no deberia de actualizarse aqui el ultimo octeto
    nuevoOCteto = ultimoOctetoUsado+1
    CA.upgradeNewClienteInProviderEdge(ProviderEdgeNumber,nombreCliente,subinterface,nuevoOCteto)
    file.close()
    return "10."+str(ProviderEdgeNumber)+"."+str(subinterface)+"."+str(nuevoOCteto)

def getIpNetForClientEdgeInterface(ProviderEdgeNumber):
    return "10."+str(ProviderEdgeNumber)+".0.0"

def getLoopbackForClient(ProviderEdgeNumber,nombreCliente):
    X = CA.getFollowingXForClientLoopback()
    CA.upgradeNewLoopbackLANUsed(ProviderEdgeNumber,nombreCliente,X)
    return "172.16."+str(X)+".1"

def configurateClienteEdge(nombreSucursal,ProviderEdgeNumber,subinterface):
    ipaddress = getIpForVrfInClientEdge(ProviderEdgeNumber,subinterface,nombreSucursal)
    ipnet = getIpNetForClientEdgeInterface(ProviderEdgeNumber)
    loopback = getLoopbackForClient(ProviderEdgeNumber,nombreSucursal)
    X=(loopback.split("."))[2]
    texto=  "end\n" \
            "conf t\n" \
            "hostname NOMBRESUCURSAL \n" \
            "interface FastEthernet0/0\n" \
            "ip address IPADDRESSRIP 255.255.255.0\n" \
            "no shutdown\n" \
            "interface loopback 0\n" \
            "ip address LOOPBACKCLIENTE 255.255.255.0\n" \
            "exit\n" \
            "router rip\n" \
            "version 2\n" \
            "network IPNET\n" \
            "network 172.16."+str(X)+".0\n" \
            "no auto-summary\n" \
            "exit\n" \
            "do wr\n" \
            "\n"
    CA.upgradeDispositiveDataBase(nombreSucursal, str(ipaddress))
    return texto.replace("NOMBRESUCURSAL",nombreSucursal).replace("IPADDRESSRIP",ipaddress).replace("LOOPBACKCLIENTE",loopback).replace("IPNET",ipnet)

def comunicateVrfsIntoPE(VrfName1,VrfNumber1,VrfName2,VrfNumber2):
    texto="end\n" \
          "conf t\n" \
          "ip vrf VRFNAME1\n" \
          "route-target export VRFNUMBER2:VRFNUMBER2\n" \
          "route-target import VRFNUMBER2:VRFNUMBER2\n" \
          "exit\n" \
          "ip vrf VRFNAME2\n" \
          "route-target export VRFNUMBER1:VRFNUMBER1\n" \
          "route-target import VRFNUMBER1:VRFNUMBER1\n" \
          "exit\n" \
          "do wr\n" \
          "\n" \
          ""
    texto=texto.replace("VRFNAME1",VrfName1).replace("VRFNAME2",VrfName2).replace("VRFNUMBER1",str(VrfNumber1)).replace("VRFNUMBER2",str(VrfNumber2))
    return texto

def comandosInicialesSSG():
    texto = "end\n " \
            "conf t\n" \
            "service password-encyption" \
            "username ESPOL privilege 15 secret telematica" \
            "ip domain-name SW.com" \
            "crypto key generate rsa general-key modulus 1024" \
            "line vty 0 15" \
            "transport input ssh" \
            "login local" \
            "exit\n" \
            "do wr\n" \
            "\n" \
            ""
    return texto