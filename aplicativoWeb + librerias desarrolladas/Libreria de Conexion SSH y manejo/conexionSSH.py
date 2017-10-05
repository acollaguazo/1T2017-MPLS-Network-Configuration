import paramiko
import os
import sys
import time

def conectarPorSSH(ip,username,password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,port=22, username=username,password=password)
    return ssh.invoke_shell()

# @script todo el script a inyectar
# @tipoDispositivo ProviderEdge PE, Provider P
# @Numeracion 11, 1, 12, etc
def inyectarScrciptADispositivo(script,tipoDispositivo,Numeracion):
    file = open("C:/Users/Paolo/Desktop/src/restaurants/archivos/dispositivos.txt","r")
    for linea in file:
        [dispositivo,ip,username,password] = linea.strip().split(",")
        if(dispositivo == tipoDispositivo+str(Numeracion)):
            remote = conectarPorSSH(ip,username,password)
            remote.send(script)
            return
    print('No se encontro el dispositivo')

def retornarShow(Dispositivo,comandoShow):
    file = open("C:/Users/Paolo/Desktop/src/restaurants/archivos/dispositivos.txt","r")
    for linea in file:
        [dispositivo,ip,username,password] = linea.strip().split(",")
        if(dispositivo == Dispositivo):
            remote = conectarPorSSH(ip,username,password)
            stdin,stdout,stderr =remote.exec_command(comandoShow)
            time.sleep(2)
            output = stdout.readlines()
            return '\n'.join(output)
    return None