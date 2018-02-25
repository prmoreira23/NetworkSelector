# -*- coding: utf-8 -*-
import psycopg2
import commands
import sys
import os
import math
import time
from QoS import calculateQoS

def sinal():
    comando = "iwlist wlan0 scan| grep -w 'ESSID\|Signal level' | cat -n | awk '{print $2,$3,$4}'"
    resultado  = commands.getoutput(comando)
    if "Interface doesn't support scanning" not in resultado:
        resultados = resultado.split('\n')
        if(len(resultados) > 0):
            print 'Tamanho da lista', len(resultados),
            if(len(resultados) == 2):
                print resultados
            lista = []
            aux = []
            for i,val in enumerate(resultados):
                if i%2 == 0:
                    aux = []
                    aux.append(int(val.split('level=')[1]))
                else:
                    aux.append(val.split('"')[1])
                    lista.append(aux)
        else:
            return sinal()
        return lista
    else:
        return sinal()
# Funcao que realiza o cálculo do QoS
def qos(ip):
    comando = "ping -c 20 -i 0 " + ip;    
    resultado = commands.getoutput(comando);
    linhas = resultado.split('\n')
    valores = []
    for linha in linhas:
        if linha.__contains__('ttl=') and not linha.__contains__('DUP!'):
            valores.append(float(linha.split('time=')[1].split()[0])/2);
    
         
    jitter_final = 0.0
    for j in xrange(0, len(valores)-1):
        jitter = math.fabs( (valores[j+1] - valores[j] ) )
        jitter_final += jitter
    jitter_final /= len(valores)
    
    #Calculo do atraso
    atraso = (sum(valores)/len(valores) )
    
    #Calculo da Perda
    perda = 20 - len(valores)
    
    return jitter_final, atraso, perda;

# Funcao que salva os dados no banco de dados
def salvar_dados(dados):
    # Configurando uma conexao com o banco de dados
    conexao = psycopg2.connect(database="postgres", user="postgres", password="123mudar", host='localhost', port='5432')
    cursor = conexao.cursor()
    
    cursor.execute("select atualizar();");
    conexao.commit();

    # criando ponteiro para arquivo
    arq = open('dados_qos.gnu','a+')
    
    for rede in dados.keys():
        sql = "insert into redes (nome, jitter, atraso, perda, blur) values('"+rede+"', "+str(dados[rede][0])+", "+str(dados[rede][1])+", "+str(dados[rede][2])+", "+str(blur(dados[rede]))+");"
        print sql
        #arq.write('%.3f\t%.3f\t%.3f\t%.3f\n' % (dados[rede][0], dados[rede][1], dados[rede][2], blur(dados[rede])))
        cursor.execute(sql);
        conexao.commit();
    
    conexao.close()
    arq.close()
    
def salvar_sinal(lista):
    conexao = psycopg2.connect(database="postgres", user="postgres", password="123mudar", host='localhost', port='5432')
    cursor = conexao.cursor()

    cursor.execute("select atualizar();");
    conexao.commit();
    for item in lista:
        sql = "insert into redes(nome, sinal) values('"+item[1]+"', '"+str(item[0])+"')"
        cursor.execute(sql);
        conexao.commit();

    conexao.close();


"""
MAIN
"""
time.sleep(1)
print("Servidor do Site Parceiro");
usuario = commands.getoutput('whoami');

if usuario != 'root':
    print("Precisa ser root!");
    sys.exit();

# Configurando o nome do AP de acesso e o endereco em que as requisicoes ICMP serao feitas
redes = {}
#redes['GREDES_TESTE'] = '8.8.8.8';
#redes['GREDES_SMIP'] = '74.125.29.94';
#redes['GREDES_TELEMATICA'] = '74.125.29.103';
while(True):
    time.sleep(30)
    lista = sinal()
    print lista
    salvar_sinal(lista)

"""    time.sleep(20)
    iteracoes = iteracoes+1
    resultados = {}
    for rede in redes.keys():
        resultados[rede] = []
        jitter = []
        atraso = []
        perda = []
        
        for i in xrange(20):
            j, a, p = qos(redes[rede]);
            jitter.append(j);
            atraso.append(a);
            perda.append(p);
            
        resultados[rede].append(sum(jitter)/len(jitter));
        resultados[rede].append(sum(atraso)/len(atraso));
        resultados[rede].append(sum(perda)/len(perda));
        
    salvar_dados(resultados);
    """
