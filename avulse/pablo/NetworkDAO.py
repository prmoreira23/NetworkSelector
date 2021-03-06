# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode
from ConnectionFactory import ConnectionFactory
from Network import Network

class NetworkDAO(object):

    def __init__(self):
        self.connection = ConnectionFactory().getConnection()

    def getNetworkById(self, id):
        query = ("SELECT * FROM networks WHERE id = %s")        
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        net = None
        if result:
            net = Network()
            net.id = int(result[0])
            net.bssid = result[1]
            net.essid = result[2]
            net.gw = result[3]
            net.stars = int(result[4])
            net.packet_loss = float(result[5])
            net.jitter = float(result[6])
            net.delay = float(result[7])
            net.throughput = float(result[8])
            net.signal_level = float(result[9])
            net.monetary_cost = float(result[10])
            net.active = bool(result[11])
        return net

    def getAllNetworks(self):
        query = ("SELECT * FROM networks")        
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        nets = []
        for result in results:
            net = None
            if result:
                net = Network()
                net.id = int(result[0])
                net.bssid = result[1]
                net.essid = result[2]
                net.gw = result[3]
                net.stars = int(result[4])
                net.packet_loss = float(result[5])
                net.jitter = float(result[6])
                net.delay = float(result[7])
                net.throughput = float(result[8])
                net.signal_level = float(result[9])
                net.monetary_cost = float(result[10])
                net.active = bool(result[11])
                nets.append(net)
        return nets


    def getBestNetworks(self):
        query = ("SELECT * FROM networks WHERE stars = (SELECT max(stars) FROM networks)")        
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        nets = []
        for result in results:
            net = None
            if result:
                net = Network()
                net.id = int(result[0])
                net.bssid = result[1]
                net.essid = result[2]
                net.gw = result[3]
                net.stars = int(result[4])
                net.packet_loss = float(result[5])
                net.jitter = float(result[6])
                net.delay = float(result[7])
                net.throughput = float(result[8])
                net.signal_level = float(result[9])
                net.monetary_cost = float(result[10])
                net.active = bool(result[11])
                nets.append(net)
        return nets

    def getNetworkByBssid(self, bssid):
        query = ("SELECT * FROM networks WHERE bssid = %s")        
        cursor = self.connection.cursor()
        cursor.execute(query, (bssid,))
        result = cursor.fetchone()
        cursor.close()
        net = None
        if result:
            net = Network()
            net.id = int(result[0])
            net.bssid = result[1]
            net.essid = result[2]
            net.gw = result[3]
            net.stars = int(result[4])
            net.packet_loss = float(result[5])
            net.jitter = float(result[6])
            net.delay = float(result[7])
            net.throughput = float(result[8])
            net.signal_level = float(result[9])
            net.monetary_cost = float(result[10])
            net.active = bool(result[11])
        return net

    # Bug do update, AUTO_INCREMENT EH EXECUTADO
    def update(self, net, id):
        print "Updating an existing network"
        try: 
            net.id = id
            cursor = self.connection.cursor()
            query = ("UPDATE networks SET bssid=%s, essid=%s, gw=%s, stars=%s, packet_loss=%s, jitter=%s, delay=%s, throughput=%s, signal_level=%s, monetary_cost=%s, active=%s WHERE id=%s")
            cursor.execute(query, (net.bssid, net.essid, net.gw, net.stars, net.packet_loss, net.jitter, net.delay, net.throughput, net.signal_level, net.monetary_cost, True, net.id,))
            self.connection.commit()        
        except mysql.connector.Error as e:
            print "erroui", e

    def add(self, net):
        netw = self.getNetworkByBssid(net.bssid)
        if not netw:
            try:
                print "Inserting a new network"
                query = ("INSERT INTO networks (bssid, essid, gw, stars, packet_loss, jitter, delay, throughput, signal_level, monetary_cost, active) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")       
                cursor = self.connection.cursor()
                cursor.execute(query, (net.bssid, net.essid, net.gw, net.stars, net.packet_loss, net.jitter, net.delay, net.throughput, net.signal_level, net.monetary_cost, True,))
                self.connection.commit()
                net.id = cursor.lastrowid       
            except mysql.connector.Error as e:
                print "erroui", e 
        else:
            self.update(net, netw.id)

    def deactivateAllNetworks(self):
        query = ("UPDATE networks SET active=%s")       
        cursor = self.connection.cursor()
        cursor.execute(query, (False,))
        self.connection.commit()

if __name__ == '__main__':
    d = NetworkDAO()
    
    gredes_teste = Network()
    gredes_teste.bssid = "1C:4B:D6:FE:82:4F"
    gredes_teste.essid = "GREDES_TESTE"
    gredes_teste.gw = "192.169.40.1"
    d.add(gredes_teste)

    ifto = Network()
    ifto.bssid = "F8:1A:67:DC:DF:C4"
    ifto.essid = "IFTO_RDS"
    ifto.gw = "192.167.1.1"
    d.add(ifto)

    ifto_labins = Network()
    ifto_labins.bssid = "F8:1A:67:A7:CF:E8"
    ifto_labins.essid = "IFTO_LABINS"
    ifto_labins.gw = "192.167.1.1"
    d.add(ifto_labins)

    d.connection.close()
