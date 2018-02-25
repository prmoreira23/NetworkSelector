from pybrain.tools.customxml     import NetworkReader
import os

FILE_NAME = "network.xml"
STATUS = ['Bad', 'Insufficient', 'Regular', 'Good', 'Excellent']

if  os.path.isfile(FILE_NAME): 
    fnn = NetworkReader.readFrom(FILE_NAME)
else:
    print "File does not exists!!!"

to = open('nn-activated.csv', 'w')

def imprimir(lista):
    rede = fnn.activate(lista)
    maior = max(rede)
    m = [i for i,x in enumerate(rede) if x == maior]
    #print "Essa rede tem %d stars. %s.\n" %(m[0]+1, STATUS[m[0]])
    print lista, m[0]+1
    to.write("{0}, {1}, {2}, {3}, {4}, {5}, ".format(lista[0], lista[1], lista[2], lista[3], lista[4], lista[5]))
    to.write("{0}\n".format(m[0]+1))

tf = open('normalized_values.csv','r')
for line in tf.readlines():
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:6])
    #print list(indata)
    imprimir(list(indata))

tf.close()
to.close()
