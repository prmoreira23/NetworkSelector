# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Description: 
"""

import os
import time
import sys
import commands

__author__ = "Pablo Rocha Moreira"
__copyright__ = "Copyright 2014, The MobiTerm Project"
__credits__ = ["Pablo Rocha Moreira", "Claúdio de Castro Monteiro", 
                "Fábio Lima da Silva"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Pablo Rocha Moreira"
__email__ = "prm.gredes@gmail.com"
__status__ = "Development"

start_time = time.time()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def calculate_time(initial_time):
    return time.time() - initial_time

def check_privileges():
    if os.geteuid() != 0:
        exit(bcolors.FAIL + "You need to have root privileges to run this script.\nPlease try again, this time using 'sudo'. Exiting now ..." 
            + bcolors.ENDC)

def check_args():
    if len(sys.argv) != 3:
        print bcolors.FAIL + "Usage: python QoS.py [Destination IP] [Ping qtd]" + bcolors.ENDC;
        exit(0);
    
def calculate_QoS(end='8.8.8.8'):
    check_args()
    check_privileges()

    ip     = sys.argv[1] or end
    pings  = int(sys.argv[2])
    interval = 0.001

    ping_c = "ping -c {0} -i {1} {2} > pings.raw".format(pings, interval, ip)
    trans_c = "cat pings.raw | grep packets\ transmitted | awk '{print $1}'"
    recv_c = "cat pings.raw | grep packets\ transmitted | awk '{print $4}'"
    stats_c = "cat pings.raw | grep rtt | awk '{print $4}'"
    time_c = "cat pings.raw | grep packets\ transmitted | awk '{print $10}'"

    max_value    =  0.0
    total_loss   =  0
    total_delay  =  0.0
    total_jitter =  0.0
    total_throughput = 0.0 

    print 'Calculating QoS for host %s (%s) %d ICMP packets.\n' % (ip, ip, pings)
    
    try:
        os.system(ping_c)
        print "teste"
        trans_packets = int(commands.getoutput(trans_c))
        print "teste2"
        recv_packets = int(commands.getoutput(recv_c))
        print "teste3"
        stats = commands.getoutput(stats_c)
        print "teste4"
        time_t = float(commands.getoutput(time_c)[:-2])
        print "teste5"
    except ValueError:
        return {}

    print "teste6"
    print stats.split('/')

    if not len(stats):
        return {}
    
    jitter = float(stats.split('/')[3])/2
    total_jitter += jitter

    loss = trans_packets - recv_packets
    total_loss += loss

    delay = float(stats.split('/')[1])/2
    total_delay += delay

    max_value = float(stats.split('/')[2])/2 if float(stats.split('/')[2])/2 > max_value else max_value

    throughput = 128 * (float(recv_packets) / float(time_t))
    total_throughput += throughput

    #os.system("rm pings.raw")      

    #os.system("rm results")

    total_loss *= float(100)
    total_loss /= pings
    """
    print "Jitter -> %.3f\n" % (total_jitter)
    print "Delay -> %.3f\n" % (total_delay)
    print "Loss  -> %.3f %%\n" % (total_loss)
    print "Throughput -> %.3f" % (total_throughput)
    print "Highest value found: %.3f\n" % (max_value)"""

    print "--- {0} QoS statistics ---".format(ip)
    print "{0} packets transmitted, {1} received, {2}% packet loss, time {3}ms".format(trans_packets, recv_packets, total_loss, time_t)
    print "jitter/delay/ploss/throughtput = %.3f/%.3f/%.3f/%.3f" % (total_jitter, total_delay, total_loss, total_throughput)

    message = bcolors.OKGREEN + "It took %.4f seconds for the script to be executed." + bcolors.ENDC

    # print message % calculate_time(start_time)
    return {"jitter":total_jitter, "delay":total_delay, "packet_loss":total_loss, "throughput":total_throughput}


def sinal(bug_fix=0):
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
                try:
                    aux = {}
                    aux["BSSID"] = resultados[i].split('Address: ')[1]
                    aux["Signal_Level"] = int(resultados[i+1].split("Quality=")[1].split("/")[0])
                    #int(resultados[i+1].split('level=')[1].split()[0])
                    aux["ESSID"] = resultados[i+2].split('"')[1]
                    lista.append(aux)
                except:
                    return sinal(bug_fix+1) 
        else:
            return sinal(bug_fix+1)
        return lista
    else:
        return sinal(bug_fix+1)

def main():
    calculate_QoS()

if __name__ == '__main__':
    main()
