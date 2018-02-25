N_JITTER = "values/jitter_servidor.txt"
N_DELAY = "values/delay_servidor.txt"
N_PKT_LOSS = "values/perda_servidor.txt"
N_SIGNAL_LEVEL = "values/sinal_servidor.txt"

F_JITTER = open(N_JITTER)
F_DELAY = open(N_DELAY)
F_PKT_LOSS = open(N_PKT_LOSS)
F_SIGNAL_LEVEL = open(N_SIGNAL_LEVEL)

GREDES_TESTE = open("values/gredes_teste_1.csv", "w")
GREDES_NS1 = open("values/gredes_ns01.csv", "w")
GREDES_NS2 = open("values/gredes_ns02.csv", "w")

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


lista_jitter = F_JITTER.readlines()
lista_delay = F_DELAY.readlines()
lista_loss = F_PKT_LOSS.readlines()
lista_signal = F_SIGNAL_LEVEL.readlines()

for i in range(1, 885):
    jitter = lista_jitter[i].split()
    normalization(jitter, 15., 0.)
    GREDES_NS1.write("{}, ".format(jitter[0]))
    GREDES_NS2.write("{}, ".format(jitter[1]))
    GREDES_TESTE.write("{}, ".format(jitter[2]))

    delay = lista_delay[i].split()
    normalization(delay, 15., 0.)
    GREDES_NS1.write("{}, ".format(delay[0]))
    GREDES_NS2.write("{}, ".format(delay[1]))
    GREDES_TESTE.write("{}, ".format(delay[2]))

    loss = lista_loss[i].split()
    normalization(loss, 100., 0.)
    GREDES_NS1.write("{}, ".format(loss[0]))
    GREDES_NS2.write("{}, ".format(loss[1]))
    GREDES_TESTE.write("{}, ".format(loss[2]))

    signal = lista_signal[i].split()
    normalization(signal, 70.0, 0.)
    GREDES_NS1.write("{}, ".format(signal[0]))
    GREDES_NS2.write("{}, ".format(signal[1]))
    GREDES_TESTE.write("{}, ".format(signal[2]))

    value = [10000,] 
    normalization(value, 15000., 0.)
    GREDES_NS1.write("{}, ".format(value[0]))
    GREDES_NS2.write("{}, ".format(value[0]))
    GREDES_TESTE.write("{}, ".format(value[0],))

    GREDES_NS1.write("{}\n".format(0))
    GREDES_NS2.write("{}\n".format(0))
    GREDES_TESTE.write("{}\n".format(0))

GREDES_TESTE.close()
GREDES_NS1.close()
GREDES_NS2.close()
