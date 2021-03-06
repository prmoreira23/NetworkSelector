from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.customxml     import NetworkWriter
from pybrain.tools.customxml     import NetworkReader
import os
import pylab as pl

FILE_NAME = "network.xml"
CLASSES = ["Bad", "Insufficient", "Regular", "Good", "Excellent"]

ds = ClassificationDataSet(6, 1, nb_classes=len(CLASSES), class_labels=CLASSES)

tf = open('datasets/dataset_normalized.csv','r')
log = open("class1.log", "w")

print "Reading dataset from file...",

E = 100.0

for line in tf.readlines():
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:6])
    outdata = tuple(int (x) for x in data[6:])
    ds.addSample(indata, outdata)

print "done."
tf.close()

print "Trainning"
tstdata, trndata = ds.splitWithProportion(0.25)

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

if os.path.isfile(FILE_NAME): 
    fnn = NetworkReader.readFrom(FILE_NAME) 
else:
    fnn = buildNetwork(trndata.indim, 6, trndata.outdim, outclass=SoftmaxLayer)

trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, learningrate=0.001 , verbose=True, weightdecay=0.01) 

gravar = True

for i in range(1000):
    error = float(trainer.train())
    #trainer.trainEpochs(900)
    #trainer.trainUntilConvergence() 
    percent = percentError(trainer.testOnClassData(dataset=tstdata), tstdata['class'])
    print 'Percent Error on Test dataset: ', percent 
    
    log.write("Epoch: {0}  --  Train Error: {1} %  --  Test Train Error: {2} %\n".format(i+1, "%.2f" % (error * 100), percent))
    log.flush()

    if percent < E:
        E = percent
        NetworkWriter.writeToFile(fnn, FILE_NAME)
        log.write("Saving NN to XML file... error: {} %\n".format(percent))
        log.flush()
        gravar = False

if gravar:
    NetworkWriter.writeToFile(fnn, FILE_NAME)
log.close()
