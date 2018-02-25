import commands
import os

while True:
    comando = "iwconfig | grep wlan | cut -c -5"    
    output = commands.getoutput(comando)
    redes = output.split("extensions.")[-1].split()
    os.system("clear")
    for rede in redes:
        print rede
    print ""
