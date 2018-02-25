FILE = open("captura.csv")

ARQUIVO = open("normalized_values.csv", "w")

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

for line in FILE.readlines():
    values = line.split(",")
    jitter = [float(values[0]),]    
    normalization(jitter, 15., 0.)
    ARQUIVO.write("{}, ".format(jitter[0]))

    delay = [float(values[1]),]
    normalization(delay, 15., 0.)
    ARQUIVO.write("{}, ".format(delay[0]))

    loss = [float(values[2]),]
    normalization(loss, 100., 0.)
    ARQUIVO.write("{}, ".format(loss[0]))

    signal = [float(values[3]),]
    normalization(signal, 70.0, 0.)
    ARQUIVO.write("{}, ".format(signal[0]))

    throughput = [10000,] 
    normalization(throughput, 15000., 0.)
    ARQUIVO.write("{}, ".format(throughput[0]))

    ARQUIVO.write("{}\n".format(0))

ARQUIVO.close()
FILE.close()
