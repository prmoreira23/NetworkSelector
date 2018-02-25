import socket, platform, urllib2, os, time
import sys
#pega a quantidade de itens passsados por parametro
x = len(sys.argv)
if x < 6:
    print '\n' 'cliente_video [n vezes] [arquivo_orig] [.formato_original] [.formato_p_conversao] [protocolo]' '\n'
    exit(0)
vezes = sys.argv[1]
vezes = int(vezes)
arquivo_orig = sys.argv[2]
formato = sys.argv[3]
formato_c = (sys.argv[4])
protocolo = sys.argv[5]

print 'INICIO DO PROGRAMA'
i = 0
y = 1

#cria um arquivo chamado dados
os.system("echo "" > dados")
while i < 1:

#	COMANDOS
	comando3 = "mv /home/aluno/Testes/videos/*"
	comando3 += formato + " /home/aluno/Testes/t/"
	print 'O comando ficou assim: ', comando3
	#comeca a chamada
	p = 1 
#	CHAMAR E GRAVAR OS VIDEOS
	while p <= vezes:
		if (protocolo == "rtsp" or protocolo == "RTSP"):
                        comando1 = "vlc --play-and-exit rtsp://1.1.1.2:5555/flower --sout /home/aluno/Testes/videos/v"
                elif (protocolo == "http" or protocolo == "HTTP"):
                        comando1 = "vlc --play-and-exit http://1.1.1.2:5555 --sout /home/aluno/Testes/videos/v"

		p = str(p)
		comando1 += p +	formato + " &"
		print 'comando1: ', comando1
		time.sleep(2)
		os.system(comando1)
		p = int(p)
		p += 1
		comando1 = ""
		n = ""
		o = 0		
		while o == 0:
			os.system("ps aux | grep vlc | grep Sl | wc -l > gatilho")
			r=open("gatilho", "r")
			rg = r.readline()
			r.close()
			rg = int(rg)
#		LEMBRA DE MUDAR PARA UM A LINHA ABRAIXO QUANDO ESTA MAQ. NAO FOR O SERVIDOR.
			rg -= 1
			print 'Quantidade de VLC em execucao: ', rg
			if rg >10:
				print 'Vou esperar por 5 segundos'
				time.sleep(5)
			else:
				o = 1 
	print 'Sai do loop que chama mais um video!' 
	time.sleep(3)
	u = 0
	while u == 0:
		l = 10
		os.system("ps aux | grep vlc | grep Sl | wc -l > gatilho")
		r=open("gatilho", "r")
		rg = r.readline()
		r.close()
		rg = int(rg)
#		LEMBRA DE MUDAR PARA UM A LINHA ABRAIXO QUANDO ESTA MAQ. NAO FOR O SERVIDOR.
		rg -= 1
		print 'Videos restantes', rg
		while rg == 0:
#			move todos os videos
			os.system(comando3)
			rg = 2

#			calcula o psnr de todos os videos
			s = 1
			while s < p:
				s = str(s)
				comando5 = "ffmpeg -i " + " /home/aluno/Testes/t/v"
				comando5 += s + formato + " /home/aluno/Testes/y/v" + s + formato_c
				print 'comando5: ', comando5
				time.sleep(3)
				os.system(comando5)
				comando6 = "./tiny " + arquivo_orig + formato_c
				comando6 += " /home/aluno/Testes/y/v"
				s = str(s)
				comando6 += s + formato_c + " >> dados"
				print 'comando6:', comando6
				time.sleep(3)
				os.system(comando6)
				s = int(s)
				s += 1		
				u += 1
	i += 1
	y += 1
	print 'FIM DO LOOP'
