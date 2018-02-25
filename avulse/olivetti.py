from sklearn import datasets
olivetti = datasets.fetch_olivetti_faces()
X, y = olivetti.data, olivetti.target

from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer
from pybrain.tools.customxml import NetworkWriter
from pybrain.tools.customxml import NetworkReader
from numpy import ravel
import os

ds = ClassificationDataSet(4096, 1 , nb_classes=40)
for k in xrange(len(X)): 
    ds.addSample(ravel(X[k]),y[k]) # ravel returns a flattenned array

tstdata, trndata = ds.splitWithProportion(0.25)

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

#print trndata['input'], trndata['target'], tstdata.indim, tstdata.outdim

fnn = buildNetwork( trndata.indim, 64 , trndata.outdim, outclass=SoftmaxLayer )
trainer = BackpropTrainer( fnn, dataset=trndata, momentum=0.1, learningrate=0.01 , verbose=True, weightdecay=0.01)

if  os.path.isfile('oliv.xml'): 
    fnn = NetworkReader.readFrom('oliv.xml') 
else:
    fnn = buildNetwork(trndata.indim, 64 , trndata.outdim, outclass=SoftmaxLayer)

for i in range(1000):
    error = trainer.trainEpochs()
    print 'Epoch: ', i+1, 'Percent Error on Test dataset: ' , percentError( trainer.testOnClassData (
           dataset=tstdata )
           , tstdata['class'] )

NetworkWriter.writeToFile(fnn, 'oliv.xml')