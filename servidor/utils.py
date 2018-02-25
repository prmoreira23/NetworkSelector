from QoS import calculate_QoS, sinal
import commands
import os, time, sys
from NetworkDAO import NetworkDAO
from Classifier import Classifier
from Network import Network

redes = {"GREDES_TESTE":None, "IFTO":None, "IFTO_LABINS":None}
gateways = {"GREDES_TESTE":"192.169.40.1", "IFTO":"192.167.1.1", "IFTO_LABINS":"192.167.1.1"}

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def is_root():
    usuario = commands.getoutput('whoami')
    if usuario != 'root':
        print(bcolors.WARNING+"Need to be root!"+bcolors.ENDC)
        sys.exit()

def turn_on_wifi():
    commands.getoutput("nmcli nm enable true 2>> error.out/connect;nmcli nm wifi on 2>> error.out/wifi")

def availableIfaces():
    comando = "iwconfig | grep wlan | cut -c -5"    
    output = commands.getoutput(comando)
    ifaces = output.split("extensions.")[-1].split()
    os.system("clear")
    return ifaces

def split(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0
    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg
    return out

def collector(n, interface, network):
    print "Collector {0} using interface {1} [collecting data from {2}]".format(n+1, interface, network[0].essid)
    n = network[0]
    dao = NetworkDAO()
    c = Classifier()
    count = 0

    while(True):
        time.sleep(5)
        redes = sinal()
        #d.deactivateAllNetworks()
        for rede in redes:
            # {"jitter":total_jitter, "delay":total_delay, "packet_loss":total_loss, "throughput":total_throughput}
            if rede["ESSID"] <> n.essid: continue
            qos = calculate_QoS(interface, n.gw)
            if not qos:
                print "Something went wrong %d."%(count+1)
                if count == 2:
                    count = -1
                    connect(interface, n.essid)
                    time.sleep(5)
                count += 1
                continue
            n.packet_loss = qos["packet_loss"]
            n.jitter = qos["jitter"]
            n.delay = qos["delay"]            
            n.signal_level = rede["Signal_Level"]
            c.classify(n)
            dao.add(n)
            return

def connect(iface, essid, password=None):
    if password:
        os.system("nmcli d wifi connect {0} password {1} iface {2} 2>> error.out/erro".format(essid, password, iface))
    else:
        os.system("nmcli d wifi connect {0} iface {1} 2>> error.out/erro2".format(essid, iface))
    time.sleep(5)

def disconnect(iface):
    os.system("nmcli dev disconnect iface {0} --nowait 2>> error.out/disco".format(iface))
