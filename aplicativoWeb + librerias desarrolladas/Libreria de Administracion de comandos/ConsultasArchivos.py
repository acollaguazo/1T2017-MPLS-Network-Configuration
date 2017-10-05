from scripts import *
#Creando Provider

def getFollowingProviderNumber():
    file = open("archivos/Providers.txt","r")
    linea = file.readline()
    providerNumbers=0
    for linea in file:
        (providerNumbers,interface)=linea.strip().split(",")
    file.close()
    return int(providerNumbers)+1

def getProviderFollowingInterface(providerNumber):
    file = open("archivos/Providers.txt","r")
    for linea in file:
        (providerNumbers, interface) = linea.strip().split(",")
        if(providerNumbers==str(providerNumber)):
            file.close()
            if(interface=="NINGUNA"):
                file.close()
                return 0
            else:
                file.close()
                return int(interface)+1
    file.close()
    return None

def getLastProviderEdgeNumber():
    file = open("archivos/ProviderEdges.txt","r")
    for linea in file:
        if(linea!="\n"):
            valor = int(linea.strip())
    file.close()
    return valor

def generateAllVrfsForProviderEdge(ProviderEdgeNumber):
    file = open("archivos/Vrfs_Usadas.txt","r")
    temp=""
    for linea in file:
        #vrfNumber = subinterfaceUsada
        [vrfName,vrfNumber] = linea.strip().split(",")
        temp += insertVrfIntoProviderEdge(vrfName,vrfNumber,ProviderEdgeNumber)+"\n"
    file.close()
    return temp

def getFollowingXForClientLoopback():
    file = open("archivos/CE_Loopbacks.txt","r")
    X=0
    for linea in file:
        if(linea!="\n"):
           [a,b,valorX] = linea.strip().split(",")
           if(X<int(valorX)):
               X=int(valorX)
    file.close()
    return int(X)+1

def getNewVRFSucursalName(nombreCliente):
    file = open("archivos/Red_PE_Clientes.txt","r")
    lastNumber = 0
    for linea in file:
        if(linea!="\n"):
            lista = linea.strip().split(",")
            if(nombreCliente.upper() in lista[1]):
                lista = lista[1].split("_")
                number = int(lista[2])
                if(int(lastNumber)<int(number)):
                    lastNumber = int(number)
    file.close()
    return "CE_"+nombreCliente.upper()+"_"+str(lastNumber+1)

def getLastUsedVrf():
    file = open("archivos/Vrfs_Usadas.txt","r")
    number = 0
    for linea in file:
        [otro,number]=linea.strip().split(",")
    file.close()
    return int(number)

def getSubinterfaceOfAnOldClient(nombreCliente):
    file = open("archivos/Vrfs_Usadas.txt","r")
    for linea in file:
        [vrfName,vrfNumber]=linea.strip().split(",")
        if(nombreCliente in vrfName):
            file.close()
            return vrfNumber
    file.close()
    return None

def upgradeLastProviderEdgeNumber(ProviderEdgeNumber):
    file = open("archivos/ProviderEdges.txt","a")
    file.write(str(ProviderEdgeNumber)+"\n")
    file.close()

"""
Actualiza el campo de ULTIMAINTERFAZUSADA por la variable @newLasUsedInterface
Este proveedor debe estar en la base de datos, sino retorna NONE
"""
def upgradeProviderNumberDataBase(ProviderNumber,newLastUsedInterface):
    file = open("archivos/Providers.txt","r")
    DataBase=[]
    bandera = False
    for linea in file:
        LineaLista=linea.strip().split(",")
        if(LineaLista[0]==str(ProviderNumber)):
            LineaLista[1]=str(newLastUsedInterface)
            bandera = True
        DataBase.append(LineaLista)
    file.close()
    if(not bandera): #significa que el ProviderNumber enviado no existe en la DataBase
        file.close()
        return None
    file=open("archivos/Providers.txt","w")
    for lista in DataBase:
        linea = lista[0]+","+lista[1]+"\n"
        file.write(linea)
    file.close()

"""
Al crear un nuevo Provider, se necesitara configurarlo y luego de esto en la base de datos se debe crear
un registro del nuevo ProviderNumber Junto a "Ninguna" como LastUsedInterface pues en la configuracion
de un nuevo Provider no se le configura ninguna interface.
"""
def upgradeNewProviderNumberInDataBase(ProviderNumber):
    file=open("archivos/Providers.txt","a")
    file.write(str(ProviderNumber)+",NINGUNA\n")
    file.close()

def upgradeNewLoopbackLANUsed(ProviderEdgeNumber,nombreCliente,newX):
    file = open("archivos/CE_Loopbacks.txt","a")
    file.write(str(ProviderEdgeNumber)+","+str(nombreCliente)+","+str(newX)+"\n")
    file.close()

def upgradeVrfDataBase(newVrf_name,newvrfNumber):
    file = open("archivos/Vrfs_Usadas.txt", "a")
    file.write(str(newVrf_name) + "," + str(newvrfNumber) + "\n")
    file.close()

def upgradeNewClienteInProviderEdge(ProviderEdgeNumber,nombreSucursal,Subinterface,ultimoOcteto):
    file = open("archivos/Red_PE_Clientes.txt", "a")
    file.write(str(ProviderEdgeNumber) + "," + str(nombreSucursal) + "," + str(Subinterface) +","+str(ultimoOcteto) +"\n")
    file.close()

def upgradeNewSWRegistry(ProviderEdgeNumber,Port,usedVlan):
    file =open("archivos/Puertos_Switches.txt", "a")
    file.write("SW"+str(ProviderEdgeNumber) + "," + str(Port) + "," + str(usedVlan) + "\n")
    file.close()

def oldProviderEdges():
    lista = []
    file = open("archivos/ProviderEdges.txt","r")
    for PE in file:
        lista.append(str(PE.strip()))
    file.close()
    return lista

def getVrfNumber(VrfName1):
    file = open("archivos/Vrfs_Usadas.txt","r")
    for linea in file:
        [vrfName, vrfNumber] = linea.strip().split(",")
        if(vrfName == VrfName1):
            file.close()
            return vrfNumber
    file.close()
    print(VrfName1+" NOT IN THE VRF DATA BASE")
    return None

def getLastSwitchportUsed(ProviderEdgeNumber):
    file = open("archivos/Puertos_Switches.txt","r")
    SW = "SW"+str(ProviderEdgeNumber)
    ultimoPuerto = 0
    for linea in file:
        [switch,port,vlan]=linea.strip().split(",")
        if(switch==SW and int(port)>ultimoPuerto):
            ultimoPuerto=int(port)
    file.close()
    return ultimoPuerto

def upgradeDispositiveDataBase(Dispositive,ip,username="ESPOL",password="telematica"):
    file = open("archivos/dispositivos.txt","a")
    string =  str(Dispositive)+","+str(ip)+","+str(username)+","+str(password)+"\n"
    file.write(string)
    file.close()
