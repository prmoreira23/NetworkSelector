from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure import SoftmaxLayer

net = buildNetwork(2, 3, 2, hiddenclass=TanhLayer, outclass=SoftmaxLayer, bias=True)



