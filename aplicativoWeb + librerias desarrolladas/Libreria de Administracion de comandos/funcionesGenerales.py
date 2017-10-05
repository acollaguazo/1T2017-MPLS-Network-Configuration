import ConsultasArchivos as CA
import scripts as sc



# ProviderNumber es extraido desde el aplicativo web.
# El usuario debe senalar a que provider estara unido este nuevo ProviderEdge
def addProviderEdgeWithOUTClient(ProviderNumber):                   #usuario,contrasena=>TELEMATICA,TELEMATICA   sector
    newProviderEdgeNumber = int(CA.getLastProviderEdgeNumber())+1
    newInterfaceInProvider = CA.getProviderFollowingInterface(ProviderNumber)
    script = sc.newInterfaceForProvider(newInterfaceInProvider,newProviderEdgeNumber,ProviderNumber)
    #ssh.inyectarScrciptADispositivo(script,"P",ProviderNumber)
    print (script)
    print ("=================================================================\n\n\n\n")
    script = sc.inicializeProviderEdge(newProviderEdgeNumber,ProviderNumber)
    script += "\n"+CA.generateAllVrfsForProviderEdge(newProviderEdgeNumber)
    file = open("equiposNuevo/PE"+str(newProviderEdgeNumber)+".txt","w")
    file.write(sc.comandosInicialesSSG()+"\n"+script)
    file.close()
    lista = CA.oldProviderEdges()
    CA.upgradeLastProviderEdgeNumber(newProviderEdgeNumber)
    script = sc.providerEdgesUpgradeForNewProviderEdge(newProviderEdgeNumber)
    #provider Edges Anteriores
    for PE in lista:
        print (script)
        print ("=================================================================\n\n\n\n")
        #ssh.inyectarScrciptADispositivo(script,"PE",PE)
    CA.upgradeProviderNumberDataBase(ProviderNumber,newInterfaceInProvider)
    return int(newProviderEdgeNumber)

def addClientToProviderEdge(ProviderEdgeNumber,nombreCliente,nuevo):
    if(not nuevo):
        subinterface = CA.getSubinterfaceOfAnOldClient(nombreCliente)
        if(subinterface!=None):
            nombreSucursal=CA.getNewVRFSucursalName(nombreCliente)
            #NombreSucursal es CE_nombreCliente_Numeracion
        else:
            print("No se encontro tal cliente en addProviderEdgeWithCliente")
            return
    else:
        lastVrf = int(CA.getLastUsedVrf())   #al ser nueva VRF, primero obtengo el ultimo vrfNumber de la base de datos
        subinterface = lastVrf+1            #La subinterface a usarse, igual que la VLAN y que la VRFnumber seran la ultima vrfNumber +1
        newVrfName = "CE_"+nombreCliente    #El nombre de la VRF es CE_+nombreCLiente
        CA.upgradeVrfDataBase(newVrfName,subinterface)   #Anado a la base de datos de las VRFs la nueva creada
        nombreSucursal=newVrfName+"_1"                   # Se anade el 1 como numero pues es el primero ya que es nueva VRF y se crea el nombreSucursal
        oldProviderEdgesList = CA.oldProviderEdges()     #Obtengo el listado de todas las numeraciones de PEs ya establecidos... aqui ingresa la que se configuro hace unos momentos pues esta tampoco tiene esta nueva VRF
        #olProviderEdges retorna un listado de ProviderEdgeNumbers con el nuevo ProviderEdgeCreado, se procedera a hacer la conexion SSH a todos los PE y crear la VRF nueva
        for PE in oldProviderEdgesList:    #Se agrega a todos los PE la nueva vrf, con los comandos necesarios en la variables @script
            script = sc.insertVrfIntoProviderEdge(newVrfName,subinterface,PE)
            #ssh.inyectarScrciptADispositivo(script,"PE",PE)
            print ("=================================================================\n\n\n\n")
            print (script)
    #Conexion SSH al dispositivo nuevaSucursal
    script = sc.configurateClienteEdge(nombreSucursal,ProviderEdgeNumber,subinterface)   #Ahora @Script almacena los comando necesarios para crear un nuevo cliente en un PE establecido
    file = open("equiposNuevo/" + nombreSucursal+".txt", "w")
    file.write(sc.comandosInicialesSSG()+"\n"+script)
    file.close()
    interfaceDelSwitchAUsar = CA.getLastSwitchportUsed(ProviderEdgeNumber)+1
    CA.upgradeNewSWRegistry(ProviderEdgeNumber,interfaceDelSwitchAUsar,subinterface)

#@nombreCliente = TROPIBURGER
#@nuevo  True si es un nuevo cliente y nombreCliente sera un Cliente nuevo, por ejemplo "FARMACIS". Caso de ser False siginifica que "FARMACIS" ya  existe en base
#@PoviderNumber numero del Provider al cual se conectara el Provider Edge Nuevo
def addProviderEdgeWithClient(ProviderNumber,nombreCliente,nuevo):
    ProviderEdgeNumber = addProviderEdgeWithOUTClient(ProviderNumber)
    addClientToProviderEdge(ProviderEdgeNumber,nombreCliente,nuevo)

#La comunicacion entre los clientes se basara en la posibilidad de importar y exportar paquetes entre vrf.
#Cada PE se encarga de tener creada una vrf para cada cliente y por la cual las sucursales de este cliente pasan para pasar los paquetes
#Para comunicar vrfs entre 2 PE se debera asignar a sus vrfs la capacidad de importar y exportar la otra vrf y viceversa.
#Por ende para comunicar 2 vrfs se necesitara los vrfName y vrfNumber de cada vrf y selecciona entre que PEs se quiere hacer comunicacion
def ComunicateVrfsInProviderEdges(VrfName1,VrfName2,*listadoDeProviderEdgeNumbers):
    VrfNumber1=CA.getVrfNumber(VrfName1)
    VrfNumber2=CA.getVrfNumber(VrfName2)
    script = sc.comunicateVrfsIntoPE(VrfName1,VrfNumber1,VrfName2,VrfNumber2)
    print ("=================================================================\n\n\n\n")
    #Estos comandos van en cada uno de los PE que se quiera que exista comunicacione entre las VRFs deseadas
    for ProviderEdgeNumber in listadoDeProviderEdgeNumbers:
        print (script)
        print ("=================================================================\n\n\n\n")
        #ssh.inyectarScrciptADispositivo(script,"PE",ProviderEdgeNumber)
        pass

def presentarShow(Dispositivo,comandoShow):
    lineas = ssh.retornarShow(Dispositivo,comandoShow)
    if(lineas==None):
        lineas = 'DISPOSITIVO NO ENCONTRADO, FAVOR VALIDAR'
    return lineas
