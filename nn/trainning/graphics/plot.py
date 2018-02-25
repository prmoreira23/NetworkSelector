import pylab
import numpy as np
import os

comando = "cat trainning.log | grep -w 'Test Train Error:' > res.out"

os.system(comando)

resultados = open("res.out", "r")

pylab.xlabel('Epochs')
pylab.ylabel('Error on Validation Dataset (%)')
pylab.title('Network Classification Neurons 6-6-5')

x = []
y = []

ax = open("X.txt", "w")
ay = open("Y.txt", "w")

for r in resultados:
    x_i = int(r.split(" ")[1])
    y_i = float(r.split(" ")[15])
    x.append(x_i)
    y.append(y_i)
    ax.write("%d\n" % (x_i))
    ay.write("%f\n" % (y_i))



resultados.close()
ax.close()
ay.close()

pylab.xlim(0, 1000)
pylab.xticks([i for i in range(50, 1000, 100)])
pylab.ylim(0, 40)
pylab.yticks([i for i in range(0, 41, 5)])

print len(x), len(y)

pylab.plot(x, y)
pylab.show()
