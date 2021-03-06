import socket
import sys
import os
import json

from NetworkDAO import NetworkDAO

d = NetworkDAO()

print "Programa Servidor de Sockets."

ip = '127.0.0.1' # vazio para usar o endereco do servidor
porta = 6666 # porta que ficara escutando as requisicoes

# Criando o socket
try:
    meu_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket UDP
except socket.error:
    print "Erro ao criar socket!"
    sys.exit(1)

# Faz o socket ficar esperando as requisicoes
meu_socket.bind((ip,porta))


while True:
    mensagem, endereco = meu_socket.recvfrom(1024)
    print mensagem
    if mensagem == 'OK':
        print 'ok'
        dados = str(d.getAllNetworks());
        print 'ola', dados
        #print dados
        arq = open('arquivo.log','a+')
        arq.write(str(endereco[0])+':'+str(endereco[1])+'\n')
        arq.close()
        print endereco,'\n'
        # Envia os dados para quem requisitou
        meu_socket.sendto(dados, endereco)
meu_socket.close()
print('Programa encerrado!')
