from pybrain.datasets            import ClassificationDataSet
from pybrain.utilities           import percentError
from pybrain.tools.shortcuts     import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure.modules   import SoftmaxLayer

alldata = ClassificationDataSet(6, 1, nb_classes=5)

tf = open('dataset.csv','r')
log = open("classification.log", "w")

print "Reading dataset from file...",

for line in tf.readlines():
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:6])
    outdata = tuple(int (x) for x in data[6:])
    alldata.addSample(indata, outdata)

print "done."
tf.close()

tstdata, trndata = alldata.splitWithProportion(0.25)

trndata._convertToOneOfMany()
tstdata._convertToOneOfMany()

print "Number of training patterns: ", len(trndata)
print "Input and output dimensions: ", trndata.indim, trndata.outdim
print "First sample (input, target, class):"
print trndata['input'][0], trndata['target'][0], trndata['class'][0]

fnn = buildNetwork(trndata.indim, 10, 10, 5, 3, 2, trndata.outdim, outclass=SoftmaxLayer)

trainer = BackpropTrainer(fnn, dataset=trndata, momentum=0.1, verbose=True, weightdecay=0.01)

for i in range(20):
    trainer.trainEpochs( 1 )
    trnresult = percentError(trainer.testOnClassData(), trndata['class'] )
    tstresult = percentError(trainer.testOnClassData(dataset=tstdata ), tstdata['class'])

    log.write("Epoch: %d  --  Train Error: %.2f --  Test Error: %.2f\n".format(i+1, trnresult, tstresult))
    log.flush()

    print "epoch: %4d" % trainer.totalepochs, \
          "  train error: %5.2f%%" % trnresult, \
          "  test error: %5.2f%%" % tstresult
log.close()