# -*- coding: utf-8 -*-
import json

__author__ = "Pablo Rocha Moreira"
__copyright__ = "Copyright 2014, The MobiTerm Project"
__credits__ = ["Pablo Rocha Moreira", "Claúdio de Castro Monteiro"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Pablo Rocha Moreira"
__email__ = "prm.gredes@gmail.com"
__status__ = "Development"

class Network(object):
    def __init__(self):
        self.id = None
        self.bssid = ""
        self.essid = ""
        self.gw = "8.8.8.8"
        self.stars = 1
        self.packet_loss = 0
        self.jitter = 0
        self.delay = 0
        self.throughput = 10000
        self.signal_level = 0
        self.monetary_cost = 0

    def __repr__(self):
        return json.dumps(self.__dict__)

    def __str__(self):
    	return self.__repr__()