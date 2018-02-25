print("\nImporting training data...")
from pybrain.datasets import ClassificationDataSet
#bring in data from training file
CLASSES = ["Bad", "Insufficient", "Regular", "Good", "Excellent"]

traindata = ClassificationDataSet(6, 1, nb_classes=len(CLASSES), class_labels=CLASSES)
f = open('dataset.csv','r')

for line in f.readlines():
    data = [float(x) for x in line.strip().split(',') if x != '']
    indata =  tuple(data[:6])
    outdata = tuple(int (x) for x in data[6:])
    traindata.addSample(indata, outdata)

f.close()

print("Training rows: %d " %  len(traindata) )
print("Input dimensions: %d, output dimensions: %d" % ( traindata.indim, traindata.outdim))
#convert to have 1 in column per class
traindata._convertToOneOfMany()
#raw_input("Press Enter to view training data...")
#print(traindata)
print("\nFirst sample: ", traindata['input'][0], traindata['target'][0], traindata['class'][0])

print("\nCreating Neural Network:")
#create the network
from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules import SoftmaxLayer
#change the number below for neurons in hidden layer
hiddenneurons = 2
net = buildNetwork(traindata.indim,hiddenneurons,traindata.outdim, outclass=SoftmaxLayer)
print('Network Structure:')
print('\nInput: ', net['in'])
#can't figure out how to get hidden neuron count, so making it a variable to print
print('Hidden layer 1: ', net['hidden0'], ", Neurons: ", hiddenneurons )
print('Output: ', net['out'])

#raw_input("Press Enter to train network...")
#train neural network
print("\nTraining the neural network...")
from pybrain.supervised.trainers import BackpropTrainer
trainer = BackpropTrainer(net,traindata)
trainer.trainUntilConvergence(dataset = traindata, maxEpochs=100, continueEpochs=10, verbose=True, validationProportion = .20)

print("\n")
for mod in net.modules:
    for conn in net.connections[mod]:
        print conn
        for cc in range(len(conn.params)):
            print conn.whichBuffers(cc), conn.params[cc]

print("\nTraining Epochs: %d" % trainer.totalepochs)

from pybrain.utilities import percentError
trnresult = percentError( trainer.testOnClassData(dataset = traindata),
                              traindata['class'] )
print("  train error: %5.2f%%" % trnresult)
#result for each class
trn0, trn1 =  traindata.splitByClass(0)
trn0result = percentError( trainer.testOnClassData(dataset = trn0), trn0['class'])
trn1result = percentError( trainer.testOnClassData(dataset = trn1), trn1['class'])
print("  train class 0 samples: %d, error: %5.2f%%" % (len(trn0),trn0result))
print("  train class 1 samples: %d, error: %5.2f%%" % (len(trn1),trn1result))

raw_input("\nPress Enter to start testing...")

print("\nImporting testing data...")
#bring in data from testing file
testdata = ClassificationDataSet(2,1,2)
f = open("dataset.csv")
for line in f.readlines():
    #using classification data set this time (subtracting 1 so first class is 0)
    testdata.appendLinked(list(map(float, line.split()))[0:2],int(list(map(float, line.split()))[2])-1)
    

print("Test rows: %d " %  len(testdata) )
print("Input dimensions: %d, output dimensions: %d" % ( testdata.indim, testdata.outdim))
#convert to have 1 in column per class
testdata._convertToOneOfMany()
#raw_input("Press Enter to view training data...")
#print(traindata)
print("\nFirst sample: ", testdata['input'][0], testdata['target'][0], testdata['class'][0])

print("\nTesting...")
tstresult = percentError( trainer.testOnClassData(dataset = testdata),
                              testdata['class'] )
print("  test error: %5.2f%%" % tstresult)
#result for each class
tst0, tst1 =  testdata.splitByClass(0)
tst0result = percentError( trainer.testOnClassData(dataset = tst0), tst0['class'])
tst1result = percentError( trainer.testOnClassData(dataset = tst1), tst1['class'])
print("  test class 0 samples: %d, error: %5.2f%%" % (len(tst0),tst0result))
print("  test class 1 samples: %d, error: %5.2f%%" % (len(tst1),tst1result))