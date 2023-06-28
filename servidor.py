import os
import socket
import threading
from colorama import Fore, Style

estilo = Style.BRIGHT
verde = Fore.GREEN
rojo = Fore.RED
amarillo = Fore.YELLOW
cian = Fore.CYAN
azul = Fore.BLUE
magenta = Fore.MAGENTA

os.system('cls')

class servidorChat:
    def __init__(self) -> str:
        self.host = input(f'{amarillo}[+] IP del servidor:{rojo} ')
        self.port = int(input(f'{amarillo}[+] Puerto:{rojo} '))
        
        self.servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.servidor.bind((self.host, self.port))
        self.servidor.listen()
        print(estilo + azul + f'servidor corriendo en {verde}{self.host}{rojo}:{verde}{self.port} ')
        
        self.clientes = []
        self.usuarios = []
        
    def transmision(self, mensaje, _cliente):
        for cliente in self.clientes:
            if cliente != _cliente:
                cliente.send(mensaje)
    
    def manejar_mensajes(self, cliente):
        while True:
            try:
                mensaje = cliente.recv(1024)
                self.transmision(mensaje, cliente)
                # si el usuario es nuevo se agrega a la lista de usuarios y al chat
                
            except:
                indice = self.clientes.index(cliente)
                usuario = self.usuarios[indice]
                self.transmision(f'{verde}ServerBot: {cian}{usuario} {rojo}Desconectado'.encode('utf-8'))
                self.clientes.remove(cliente)
                self.usuarios.remove(usuario)
                cliente.close()
                break
    
    def recibir_conexiones(self):
        while True:
            cliente, direccion = self.servidor.accept()
            
            cliente.send('@NickName'.encode('utf-8'))
            usuario = cliente.recv(1024).decode('utf-8')
            
            self.clientes.append(cliente)
            self.usuarios.append(usuario)
            
            print(azul + f'\n{verde}{usuario} {rojo}Conectado a {amarillo}{str(direccion)}')
            
            mensaje = f'\n{verde}ServerBot: {azul}{usuario} {verde}Se conectó al Chat!{magenta}\n'.encode('utf-8')
            self.transmision(mensaje, cliente)
            cliente.send(f'\n{cian}Te has conectado al servidor{magenta}\n'.encode('utf-8'))
            
            hilos = threading.Thread(target=self.manejar_mensajes, args=(cliente,))
            hilos.start()
            
servidor = servidorChat()
servidor.recibir_conexiones()