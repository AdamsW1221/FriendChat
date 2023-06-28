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

class ClienteChat:
    def __init__(self) -> str:
        self.usuario = input(rojo + '\nIngresa tu NickName: '+ azul)
        self.host = input(f'{cian}[+] IP del servidor:{rojo} ')
        self.port = int(input(f'{cian}[+] Puerto del servidor:{rojo} '))
        
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))
    
    def recibir_mensaje(self):
        while True:
            try:
                mensaje = self.cliente.recv(1024).decode('utf-8')
                
                if mensaje == '@NickName':
                    self.cliente.send(self.usuario.encode('utf-8'))
                else:
                    print(estilo + mensaje + '\n')
            
            except KeyboardInterrupt:
                print(estilo + rojo  + '\nOcurrió un Error')
                self.cliente.close()
                break
    
    def escribir_mensaje(self):
        while True:
            mensaje = estilo + cian + f'\n{azul}{self.usuario}: {cian}{input("->")}{magenta}'
            self.cliente.send(mensaje.encode('utf-8'))

cliente = ClienteChat()

hilo_recibir = threading.Thread(target=cliente.recibir_mensaje)
hilo_recibir.start()

hilo_escribir = threading.Thread(target=cliente.escribir_mensaje)
hilo_escribir.start()