import os, socket, json, time

pacote = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
pacote.sendto('OK', ('127.0.0.1',6666))

def recv_timeout(the_socket,timeout=0.5):
    #make socket non blocking
    the_socket.setblocking(0)
     
    #total data partwise in an array
    total_data=[];
    data='';
     
    #beginning time
    begin=time.time()
    while 1:
        #if you got some data, then break after timeout
        if total_data and time.time()-begin > timeout:
            break
         
        #if you got no data at all, wait a little longer, twice the timeout
        elif time.time()-begin > timeout*2:
            break
         
        #recv something
        try:
            data = the_socket.recv(65535)
            if data:
                total_data.append(data)
                #change the beginning time for measurement
                begin = time.time()
            else:
                #sleep for sometime to indicate a gap
                time.sleep(0.1)
        except:
            pass
     
    #join all parts to make final string
    return ''.join(total_data)

recebidos = recv_timeout(pacote)

print recebidos

pacote.close()

redes = json.loads(recebidos) or []

print redes

for rede in redes:
    print "ESSID:", rede['essid']
    print "MAC Address:", rede['bssid']
    print "QoS(packet loss/jitter/delay/throughput):", rede['packet_loss'], '/', rede['jitter'], '/', rede['delay'], '/', rede['throughput']
    print "Signal Level:", rede['signal_level']
    print "\n"
