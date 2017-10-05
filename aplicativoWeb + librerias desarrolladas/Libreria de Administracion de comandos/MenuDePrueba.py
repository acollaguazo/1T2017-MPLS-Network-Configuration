import funcionesGenerales as FG
import ConsultasArchivos as CA


bandera = True
print("BIENVENIDOS AL SISTEMA DE AUTOMATIZACION DE ADMINISTRACION DE REDES MPLS-VIEWER")
while(bandera):

    print("============================================MENU PRINCIPAL======================================")
    print("1.- Ingresar un nuevo Provider Edge con un Cliente antiguo\n"
          "2.- Ingresar un nuevo Provider Edge con un Cliente nuevo\n"
          "3.- Ingresar una nueva sucursal de Cliente antiguo\n"
          "4.- Ingresar una nueva sucursal de Cliente nuevo\n"
          "5.- Comunicar VRF1 con VRF2 en Provider Edges\n"
          "6.- Salir del sistema\n")
    op = input("Escoja una de las opciones: ")

    if (op == "1"):
        providerNumber = input("Favor ingresar el numero del proveedor a conectarse: ")
        nombreCliente = input("Favor ingresar el nombre del cliente antiguo: ").upper()
        valor = False
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("           COMANDOS DE LOS DISPOSITIVOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
        FG.addProviderEdgeWithClient(providerNumber, nombreCliente, False)
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("                 FIN DE LOS COMANDOS")
        print("==========================================================")
        print("==========================================================\n\n\n")

    elif(op=="2"):
        providerNumber = input("Favor ingresar el numero del proveedor a conectarse: ")
        nombreCliente = input("Favor ingresar el nombre del cliente nuevo: ").upper()
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("           COMANDOS DE LOS DISPOSITIVOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
        FG.addProviderEdgeWithClient(providerNumber, nombreCliente, True)
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("                 FIN DE LOS COMANDOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
    elif(op=="3"):
        ProviderEdgeNumber = input("Favor ingresar el numero del PROVIDER EDGE a conectarse: ")
        nombreCliente = input("Favor ingresar el nombre del cliente antiguo: ").upper()
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("           COMANDOS DE LOS DISPOSITIVOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
        FG.addClientToProviderEdge(ProviderEdgeNumber, nombreCliente, False)
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("                 FIN DE LOS COMANDOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
    elif(op=="4"):
        ProviderEdgeNumber = input("Favor ingresar el numero del PROVIDER EDGE a conectarse: ")
        nombreCliente = input("Favor ingresar el nombre del cliente nuevo: ").upper()
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("           COMANDOS DE LOS DISPOSITIVOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
        FG.addClientToProviderEdge(ProviderEdgeNumber, nombreCliente, True)
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("                 FIN DE LOS COMANDOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
    elif (op == "5"):
        vrfName1 = "CE_"+input("INGRESE EL NOMBRE DEL CLIENTE 1 A CONECTAR").strip()
        vrfName2 = "CE_"+input("INGRESE EL NOMBRE DEL CLIENTE 2 A CONECTAR").strip()
        providerEdgeNumber1 = input("INGRESE NUMERACION DE PROVIDER EDGE 1 A CONECTAR: ")
        providerEdgeNumber2 = input("INGRESE NUMERACION DE PROVIDER EDGE 2 A CONECTAR: ")
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("           COMANDOS DE LOS DISPOSITIVOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
        FG.ComunicateVrfsInProviderEdges(vrfName1,vrfName2,providerEdgeNumber1,providerEdgeNumber2)
        print("\n\n\n==========================================================")
        print("==========================================================")
        print("                 FIN DE LOS COMANDOS")
        print("==========================================================")
        print("==========================================================\n\n\n")
    elif(op=="6"):
        print("\n\n\n===============SALIENDO DEL SISTEMA DE AUTOMATICACION DE REDES MPLS - VIEWER===================\n\n\n")
        bandera = False
    else:
        print("\n\n\n==============FAVOR INGRESAR SOLAMENTE UNA DE LAS OPCIONES VISTAS EN PANTALLA==================\n\n\n")

