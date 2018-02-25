# -*- coding: utf-8 -*-
#import psycopg2
import commands
import sys
import os
import math
import time
import signal

from NetworkDAO import NetworkDAO
from Network import Network
from QoS import calculateQoS

"""
FUNCOES
"""

bug_fix = 0
d = NetworkDAO()

def signal_handler(signal, frame):
    print "\nClosing connection with DB."
    d.connection.close()
    print "Exiting Now."
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def sinal():
    global bug_fix
    if bug_fix == 10: return []
    comando = "iwlist wlan0 scan | grep -w 'Address\|ESSID\|Signal level' | cut -c 21-100"
    resultado  = commands.getoutput(comando)
    if "Interface doesn't support scanning" not in resultado:
        resultados = resultado.split('\n')
        if((len(resultados) / 3) > 0):
            print 'Quantidade de Redes Escaneadas:', len(resultados) / 3
            if(len(resultados) == 3):
                print resultados
            lista = []
            for i in range(0, len(resultados), 3):
                aux = {}
                aux["BSSID"] = resultados[i].split('Address: ')[1]
                aux["Signal_Level"] = int(resultados[i+1].split('level=')[1].split()[0])
                aux["ESSID"] = resultados[i+2].split('"')[1]
                lista.append(aux)
        else:
            bug_fix+=1
            return sinal()
        return lista
    else:
        bug_fix+=1
        return sinal()

"""
MAIN
"""
time.sleep(1)
print("Servidor do Site Parceiro");

usuario = commands.getoutput('whoami');

if usuario != 'root':
    print("Precisa ser root!");
    sys.exit();

while(True):
    time.sleep(10)
    # enable Wi-Fi
    os.system("rfkill unblock wifi")
    bug_fix = 0
    redes = sinal()
    d.deactivateAllNetworks()
    for rede in redes:
        # {"jitter":total_jitter, "delay":total_delay, "packet_loss":total_loss, "throughput":total_throughput}
        qos = calculateQoS()
        print qos
        n = Network()
        n.essid = rede["ESSID"]
        n.bssid = rede["BSSID"]
        n.packet_loss = qos["packet_loss"]
        n.jitter = qos["jitter"]
        n.delay = qos["delay"]
        n.throughput = qos["throughput"]
        n.stars = 5#calculate stars for each net using trained NN
        n.signal_level = rede["Signal_Level"]
        d.add(n)

signal.pause()