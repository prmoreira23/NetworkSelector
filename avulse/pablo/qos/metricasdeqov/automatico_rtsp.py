#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys, commands, math
import os, time

# pega a quantidade de itens passados por parametro
x = len(sys.argv)
if x < 4:
    print '\n' 'automatico_rtsp [IP] [n_vezes] [nome_instancia]' '\n'
    exit(0)
user = commands.getoutput('whoami')
if user == 'root':
    print 'Não pode ser root!'
    exit(0)

# cria os diretórios necessários, caso ainda não existam
commands.getoutput("mkdir yuv mp4")
for i in xrange(0, int(sys.argv[2])):
    aux = "/v" + str(i+1) + "."
    #comando para rodar o vlc
    comando = "vlc --play-and-exit rtsp://" + sys.argv[1] + ":5555/" + sys.argv[3] + " --sout mp4" + aux + "mp4 &"
    print "Comando 1 : ",comando
    os.system(comando)
    #assim que o vlc começar a rodar, vai começar a fazer ping no servidor
    ping = "ping -i 0.2 " + sys.argv[1] + " | grep ttl | awk -F 'icmp_req=' '{print $2}' >> arq &"
    print "Comando 2 :", ping
    os.system(ping)
    #####
    qtd = 1
    while qtd:
        qtd = commands.getoutput('ps aux | grep vlc | wc -l')
        qtd = (int(qtd) - 2)
        time.sleep(1)
    os.system("kill `pidof ping`")
    #####
    #converte o vídeo mp4 para yuv
    comando = "ffmpeg -i mp4" + aux + "mp4 yuv" + aux + "yuv"
    print "Comando 3: ",comando
    os.system(comando)
    comando = "./tiny flower_cif.yuv yuv" + aux + "yuv >> resultado.txt"
    print 'Comando 4: ',comando
    os.system(comando)
    os.system('./QoS_special')
    os.system('rm arq')
    time.sleep(1)
os.system("cat -n resultado_qos| awk '{print $1, $2, $3, $4}' > resultados_qos")
os.system("cat resultado.txt | awk -F'PSNR:' '{print $2}'| cut -d' ' -f1 | cat -n | awk '{print $1, $2}' > resultados_qov")
os.system('rm resultado_qos resultado.txt')
