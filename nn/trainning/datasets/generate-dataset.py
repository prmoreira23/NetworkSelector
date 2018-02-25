from pybrain.datasets.classification import ClassificationDataSet
from random import uniform
from pybrain.tools.shortcuts import buildNetwork
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.datasets.classification import ClassificationDataSet
from pybrain.structure import SoftmaxLayer, TanhLayer
from pybrain.tools.customxml import NetworkWriter

SAMPLE_LENGTH = 20
MIL = 100
OUTPUT_FILE_NAME = "dataset.csv"
OUTPUT_FILE_NAME_2 = "dataset_normalized.csv"

jitter = []
delay = []
packet_loss = []
signal_level = []
throughput = []
cost = []
expected_result = []


output = open(OUTPUT_FILE_NAME, "w")
output2 = open(OUTPUT_FILE_NAME_2, "w")

def normalization(data, o_max, o_min, new_max=1., new_min=0.):
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

def excellent():
    # Excellent Networks
    for i in range(SAMPLE_LENGTH):
        # jitter
        sample = uniform(0, 1)
        output.write("{}, ".format(sample))
        jitter.append(sample)
        # Delay
        sample = uniform(0, 0.5)
        output.write("{}, ".format(sample))
        delay.append(sample)
        # packet loss
        sample = uniform(0, 0)
        output.write("{}, ".format(sample))
        packet_loss.append(sample)
        # signal level
        sample = uniform(60, 100)
        output.write("{}, ".format(sample))
        signal_level.append(sample)
        # throughput
        sample = uniform(5000, 15000)
        output.write("{}, ".format(sample))
        throughput.append(sample)
        # cost, per hour, MB or what???????
        sample = uniform(0, 5)
        output.write("{}, ".format(sample))
        cost.append(sample)
        expected_result.append(4)
        output.write("{}\n".format(4))
        output.flush()

def good():
    # Good Networks
    for i in range(SAMPLE_LENGTH):
        # jitter
        sample = uniform(1, 3)
        output.write("{}, ".format(sample))
        jitter.append(sample)
        # Delay
        sample = uniform(0.5, 1)
        output.write("{}, ".format(sample))
        delay.append(sample)
        # packet loss
        sample = uniform(0, 1)
        output.write("{}, ".format(sample))
        packet_loss.append(sample)
        # signal level
        sample = uniform(40, 60)
        output.write("{}, ".format(sample))
        signal_level.append(sample)
        # throughput
        sample = uniform(1500, 5000)
        output.write("{}, ".format(sample))
        throughput.append(sample)
        # cost, per hour, MB or what???????
        sample = uniform(1, 6)
        output.write("{}, ".format(sample))
        cost.append(sample)
        expected_result.append(3)
        output.write("{}\n".format(3))
        output.flush()

def regular():
    # Regular Networks
    for i in range(SAMPLE_LENGTH):
        # jitter
        sample = uniform(3, 5)
        output.write("{}, ".format(sample))
        jitter.append(sample)
        # Delay
        sample = uniform(1, 3)
        output.write("{}, ".format(sample))
        delay.append(sample)
        # packet loss
        sample = uniform(1, 3)
        output.write("{}, ".format(sample))
        packet_loss.append(sample)
        # signal level
        sample = uniform(30, 40)
        output.write("{}, ".format(sample))
        signal_level.append(sample)
        # throughput
        sample = uniform(800, 1500)
        output.write("{}, ".format(sample))
        throughput.append(sample)
        # cost, per hour, MB or what???????
        sample = uniform(2, 7)
        output.write("{}, ".format(sample))
        cost.append(sample)
        expected_result.append(2)
        output.write("{}\n".format(2))
        output.flush()

def insufficient():
    # Insufficiemte Networks
    for i in range(SAMPLE_LENGTH):
        # jitter
        sample = uniform(5, 10)
        output.write("{}, ".format(sample))
        jitter.append(sample)
        # Delay
        sample = uniform(3, 10)
        output.write("{}, ".format(sample))
        delay.append(sample)
        # packet loss
        sample = uniform(3, 10)
        output.write("{}, ".format(sample))
        packet_loss.append(sample)
        # signal level
        sample = uniform(20, 30)
        output.write("{}, ".format(sample))
        signal_level.append(sample)
        # throughput
        sample = uniform(500, 800)
        output.write("{}, ".format(sample))
        throughput.append(sample)
        # cost, per hour, MB or what???????
        sample = uniform(3, 8)
        output.write("{}, ".format(sample))
        cost.append(sample)
        expected_result.append(1)
        output.write("{}\n".format(1))
        output.flush()

def bad():
    # Bad Networks
    for i in range(SAMPLE_LENGTH):
        # jitter
        sample = uniform(10, 15)
        output.write("{}, ".format(sample))
        jitter.append(sample)
        # Delay
        sample = uniform(10, 15)
        output.write("{}, ".format(sample))
        delay.append(sample)
        # packet loss
        sample = uniform(10, 15)
        output.write("{}, ".format(sample))
        packet_loss.append(sample)
        # signal level
        sample = uniform(0, 20)
        output.write("{}, ".format(sample))
        signal_level.append(sample)
        # throughput
        sample = uniform(0, 500)
        output.write("{}, ".format(sample))
        throughput.append(sample)
        # cost, per hour, MB or what???????
        sample = uniform(4, 9)
        output.write("{}, ".format(sample))
        cost.append(sample)
        expected_result.append(0)
        output.write("{}\n".format(0))
        output.flush()

for i in range(MIL):
    bad()
    excellent()
    regular()
    good()
    insufficient()

output.close()

normalization(jitter, 15., 0.)
normalization(delay, 15., 0.)
normalization(packet_loss, 100., 0.)
normalization(signal_level, 100., 0.)
normalization(throughput, 15000., 0.)
normalization(cost, 10., 0.)

for i in range(len(jitter)):
    output2.write("{}, ".format(jitter[i]))
    output2.write("{}, ".format(delay[i]))
    output2.write("{}, ".format(packet_loss[i]))
    output2.write("{}, ".format(signal_level[i]))
    output2.write("{}, ".format(throughput[i]))
    output2.write("{}, ".format(cost[i]))
    output2.write("{}\n".format(expected_result[i]))
    output2.flush()

output2.close()
