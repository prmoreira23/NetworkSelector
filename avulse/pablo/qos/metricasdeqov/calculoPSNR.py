#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys, commands, math
import os, time

user = commands.getoutput('whoami')
if user == 'root':
    print 'Não pode ser root!'
    exit(0)

path = "/home/aluno/gabriela/metricasdeQoV"
qtdFrames = 150
executado = 1
soma = 0
print "Aguardando comparação dos frames!"
while executado <= qtdFrames:
	frame1 = path +"/videoOriginal/coco{0}.jpg".format(executado)
	frame2 = path +"/videoteste/amostradococo{0}.jpg".format(executado)
	comando = "./tiny " + frame1 + " " + frame2 + " | awk '{print $3}'"
	resultado = commands.getoutput(comando)
	if resultado == "PSNR:" or resultado == "Segmentation fault (core dumped)":
		soma += 0
	else:
		soma += float(resultado)
	executado += 1

media = soma/qtdFrames

print "\n\nMédia: {0}".format(media)
