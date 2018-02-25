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
    
def calculateQoS(end='8.8.8.8', pi=100):
   # check_args()
    check_privileges()
    try:
        ip     = sys.argv[1]
        pings  = int(sys.argv[2]) or pi
    except:
        ip     = end
        pings  = pi
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
    
    dados = open("results", "w")
    resultados = open("result", "w")
    
    try:
        os.system(ping_c)
        trans_packets = int(commands.getoutput(trans_c))
        recv_packets = int(commands.getoutput(recv_c))
        stats = commands.getoutput(stats_c)
        time_t = float(commands.getoutput(time_c)[:-2])
    except ValueError:
        exit("erro")

    #print stats.split('/')

    if not len(stats):
        exit(bcolors.FAIL + "No response.\nPlease check your internet connection. Exiting now ..." + bcolors.ENDC)
    
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
    
    dados.write("%.3f\t" % (jitter))
    dados.write("%.3f\t" % (delay))
    dados.write("%.3f\t" % (loss))
    dados.write("%.3f\t\n" % (throughput))
    dados.flush()

    dados.close()

    #os.system("rm results")

    total_loss *= float(100)
    total_loss /= pings
    """
    print "Jitter -> %.3f\n" % (total_jitter)
    print "Delay -> %.3f\n" % (total_delay)
    print "Loss  -> %.3f %%\n" % (total_loss)
    print "Throughput -> %.3f" % (total_throughput)
    print "Highest value found: %.3f\n" % (max_value)

    print "--- {0} QoS statistics ---".format(ip)
    print "{0} packets transmitted, {1} received, {2}% packet loss, time {3}ms".format(trans_packets, recv_packets, total_loss, time_t)
    print "jitter/delay/ploss/throughtput = %.3f/%.3f/%.3f/%.3f" % (total_jitter, total_delay, total_loss, total_throughput)
    """

    resultados.write("%.3f " % (total_jitter))
    resultados.write("%.3f " % (total_delay))
    resultados.write("%.3f " % (total_loss))
    resultados.write("%.3f \n" % (total_throughput))

    message = bcolors.OKGREEN + "It took %.4f seconds for the script to be executed." + bcolors.ENDC

    # print message % calculate_time(start_time)
    return {"jitter":total_jitter, "delay":total_delay, "packet_loss":total_loss, "throughput":total_throughput}

def main():
    calculateQoS()

if __name__ == '__main__':
    main()
