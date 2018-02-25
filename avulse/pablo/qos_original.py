import commands
import math
import sys

if len(sys.argv) != 4:
   print "usage <endereco ip>"
   exit(0)

print "Pingando no destino... aguarde\n"

#coleta a saida do ping
#print commands.getoutput("ping 2.2.2.2")
server = sys.argv[1]
video = sys.argv[2]
seq = sys.argv[3]

print video+seq
ping = commands.getoutput("ping %s"%server)

#corta somente os tempos de recebimento dos pacotes
tempos_ping_streaming =  commands.getoutput("echo \""+ ping+"\" | grep time= | awk -F 'time=' {'print $2'} | awk -F ' ms' {'print $1'}")
sequencia_ping_streaming =  commands.getoutput("echo \""+ ping+"\" | grep icmp_req= | awk -F 'icmp_req=' {'print $2'} | awk -F ' ' {'print $1'}")
print tempos_ping_streaming
print sequencia_ping_streaming

#transforma o array de caracter em array de string (separa os tempos)
tempos_ping = tempos_ping_streaming.split("\n")
sequencia_ping = sequencia_ping_streaming.split("\n")

#verifica se teve algum dado retornado... pelo menos 1 pacote recebido
if len(tempos_ping)<1:
    print "Destino nao encontrado ou problemas com a rede... \n"

if len(sequencia_ping)<1:
    print "Destino nao encontrado ou problemas com a rede... \n"


#armazena a soma dos tempos dos pacotes recebidos
tempo_total = 0
perda_total = 0

#calcula perda
j = int(len(sequencia_ping)-1)
perda1 = (int(sequencia_ping[j]) - int(sequencia_ping[0]))
perda_total = int(perda1-j)
print perda_total


#soma todos os tempos dos pacotes recebidos
for i in range(0, len(tempos_ping)):
   tempo_total += float(tempos_ping[i])

#faz a media dos tempos dos pacotes recebidos
media = float(tempo_total/len(tempos_ping))

#armazena o tempo do Jitter
jitter = 0

#comeca em 1, pq eh proximo menos o anterior
for j in range(1, len(tempos_ping)):        

   #soma somente o valor absoluto da diferenca entre o proximo e o anterior
   jitter += math.fabs( float( float(tempos_ping[j])-float(tempos_ping[j-1]) ) )

#tira a media da soma dos Jitter, subtraindo 1 da quantidade de pacotes recebidos
jitter = jitter/(len(tempos_ping)-1)

# Vazao 64*2*(quantidade de pacotes recebidos) / (tempo total dos pacotes)
#vazao = float( 64*2* float( len(tempos_ping) / float(tempo_total) ) )

#pega somente a quantidade de pacotes enviados (posicao 1) e recebidos (posicao 2)
# <total ' ' recebidos> , exemplo: "2 1"
#perda = commands.getoutput("echo \"" + ping +"\" | grep received | awk -F ' ' {'print $1 \" \" $4'}").split(" ")

#------------------------------------------------------------------------
#			apenas para DEPURAR				-
#------------------------------------------------------------------------
print "--------------------------------------------------------------------"
#print tempos_ping_streaming
print ping
print "--------------------------------------------------------------------"
#------------------------------------------------------------------------

var_file = open("mp4/%s/qos_log"%video+seq,"w")
var_file.write("Atraso (media): \t%.3f ms\n" %media)
#var_file.write("Tempo Total: \t\t" + str(tempo_total) +" ms\n")
var_file.write("Jitter (media): \t%.3f ms\n" %jitter)
var_file.write("Perda: \t\t\t" +str(perda_total)+ "\n")
var_file.close()

print "Atraso (media): \t%.3f ms" %media
#print "Tempo Total: \t\t" + str(tempo_total) +" ms"
print "Jitter: \t\t" + str(jitter) + " ms"
#print "Vazao: \t\t\t%.3f B/s" %vazao
print "Perda: \t\t\t" +str(perda_total)
#print "Perda de pacotes: \t"+str(int(perda[0])-int(perda[1]))
#print "Total enviado: \t\t"+perda[0]
#print "Total recebido: \t"+perda[1]
#print "QoS:\t\t\t%.2f" %(float(media+tempo_total+vazao+ (int(perda[0])-int(perda[1])) ))
