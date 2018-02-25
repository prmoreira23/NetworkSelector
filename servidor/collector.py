from threading import Thread
from utils import *
import time, os, sys, signal
from NetworkDAO import NetworkDAO
from Network import Network

FILE = "coleta.log"
f = open(FILE, "a")

def signal_handler(signal, frame):
    print "Exiting Now."
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":    
    is_root()
    turn_on_wifi()
    ifaces = availableIfaces()
    if len(ifaces) < 3: sys.exit(bcolors.FAIL+"Need at least 3 interfaces"+bcolors.ENDC)
    print "Collector is starting now... get ready for the journey!"
    ifaces.sort()

    dao = NetworkDAO()

    redes = dao.getAllNetworks()

    networks = split(redes, len(ifaces))

    message = bcolors.OKGREEN+"Connecting to {0} on {1}"+bcolors.ENDC

    for i, interface in enumerate(ifaces):
        print message.format(networks[i][0].essid, interface)
        connect(interface, networks[i][0].essid)

    time.sleep(5)
    
    while True:
        for i, interface in enumerate(ifaces):
            t = Thread(target=collector, args=(i, interface, networks[i]))
            t.start()
            t.join()
        time.sleep(2)
        print "Fim da rodada!\n\n\n"
        dao = NetworkDAO()
        best_networks = dao.getAllNetworks()
        print "As melhores redes disponiveis sao:", best_networks
        f.write(str(best_networks))
        f.write("\n")
        f.flush()

signal.pause()
