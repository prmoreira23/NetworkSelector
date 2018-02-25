# -*- coding: utf-8 -*-
from Network import Network
from pybrain.tools.customxml import NetworkReader
import os

__author__ = "Pablo Rocha Moreira"
__copyright__ = "Copyright 2014, The MobiTerm Project"
__credits__ = ["Pablo Rocha Moreira", "Claúdio de Castro Monteiro"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Pablo Rocha Moreira"
__email__ = "prm.gredes@gmail.com"
__status__ = "Development"

FILE_NAME = "network.xml"

class Classifier(object):
    def __init__(self):
        self.nn = None
        self.verify_if_nn_file_exists(FILE_NAME)

    def verify_if_nn_file_exists(self, file_name):
        if os.path.isfile(file_name): 
            self.nn = NetworkReader.readFrom(FILE_NAME)
        else:
            print "File does not exists!!!"
            sys.exit(0)

    def normalization(self, data, o_max, o_min, new_max=1., new_min=0.):
        old_max = o_max
        old_min = o_min
        old_range = (old_max - old_min)

        for i in range(len(data)):
            if old_range == 0:
                data[i] = new_min
            else:
                new_range = (new_max - new_min)
                data[i] = (((float(data[i]) - old_min) * new_range) / old_range) + new_min
                if data[i] > 1:
                    data[i] = 1.0 

    def normalize(self, lista):        
        self.normalization(lista[0], 15., 0.)
        lista[0] = lista[0][0]

        self.normalization(lista[1], 15., 0.)
        lista[1] = lista[1][0]

        self.normalization(lista[2], 100., 0.)
        lista[2] = lista[2][0]

        self.normalization(lista[3], 70., 0.)
        lista[3] = lista[3][0]

        self.normalization(lista[4], 15000., 0.)
        lista[4] = lista[4][0]

        lista[5] = lista[5][0]

    def classify(self, network):
        if not isinstance(network, Network):
            return False
        lista = []
        lista.append([network.jitter])
        lista.append([network.delay])
        lista.append([network.packet_loss])
        lista.append([network.throughput])
        lista.append([network.signal_level])
        lista.append([network.monetary_cost])
        self.normalize(lista)
        rede = self.nn.activate(lista)
        maior = max(rede)
        m = [i for i,x in enumerate(rede) if x == maior]
        network.stars = m[0] + 1
        return network.stars

if __name__ == '__main__':
    c = Classifier()
    
    gredes_teste = Network()
    gredes_teste.bssid = "1C:4B:D6:FE:82:4F"
    gredes_teste.essid = "GREDES_TESTE"
    gredes_teste.gw = "192.169.40.1"
    gredes_teste.jitter = 1.02
    gredes_teste.delay = 0.56
    gredes_teste.packet_loss = 0
    gredes_teste.signal_level = 60
    c.classify(gredes_teste)
    print gredes_teste
    

    ifto_rds = Network()
    ifto_rds.bssid = "F8:1A:67:DC:DF:C4"
    ifto_rds.essid = "IFTO_RDS"
    ifto_rds.gw = "192.167.1.1"
    ifto_rds.jitter = 5.52
    ifto_rds.delay = 2.23
    ifto_rds.packet_loss = 30
    ifto_rds.signal_level = 30
    c.classify(ifto_rds)
    print ifto_rds

    ifto_labins = Network()
    ifto_labins.bssid = "F8:1A:67:A7:CF:E8"
    ifto_labins.essid = "IFTO_LABINS"
    ifto_labins.gw = "192.167.1.1"
    ifto_labins.jitter = 200.25
    ifto_labins.delay = 150.320
    ifto_labins.packet_loss = 88
    ifto_labins.signal_level = 25
    c.classify(ifto_labins)
    print ifto_labins