/* Fabbio Lima - versao 2.0 */


#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int verify_user() {
    /* Verifica se o usuário é root, se não for, termina programa */
    FILE *user;
    system("whoami > usuario");
    user = fopen("usuario", "r");
    char usuario[15];
    fscanf(user, " %[^\n]", usuario);
    fclose(user);
    system("rm usuario");
    if (strcmp(usuario, "root") != 0) {
        return 1;
    } else {
        printf("Não pode ser root!\n");
        return 0;
    }
}


int main(int argc, char *argv[]) {
    system("clear");
    if (argc != 4) {
        printf("Insira os parâmetros corretamente!\n");
        printf("./automatico [IP] [n_vezes] [nome_instancia]\n");
        exit(0);
    }
    
            
    int quant = atoi(argv[2]), i;
    char comando[100], ping[100];
    char aux[10];
    char aux2[10];

    /* Verifica se o usuário é root, se for, termina programa */
    int user = verify_user();
    if (user != 1) {
        exit(0);
    }
    //Cria os diretórios dos vídeos, caso ainda não existam
    system("a=`mkdir yuv mp4`");
    for (i = 0; i < quant; i++) {
        //nos passos abaixo, o comando é montado para que o nome dos vídeos não repita
        sprintf(aux, "mp4/v%d.mp4", i + 1);
        strcpy(comando, "vlc --play-and-exit rtsp://");
        strcat(comando,argv[1]);
        strcat(comando, ":5555/");
        strcat(comando, argv[3]);
        strcat(comando, " --sout ");
        strcat(comando, aux);
        strcat(comando, " &");
        printf("O comando ficou assim: %s\n", comando);
        system(comando); //executa o vlc
        strcpy(ping, "ping -i 0.2 ");
        strcat(ping, argv[1]);
        strcat(ping, " | grep ttl | awk -F 'icmp_req=' '{print $2}' >> arq");
        system(ping); //executa o comando de ping -> ping -i 0.2 1.1.1.2 | grep ttl | awk -F 'icmp_req=' '{print $2}' >> arq
        //cat arq | awk -F 'icmp_req=' '{print $2}'
        strcpy(comando, "ffmpeg -i ");
        strcat(comando, aux);
        sprintf(aux2," yuv/v%d.yuv",i+1);
        strcat(comando, aux2);
        printf("O comando ficou assim: %s\n", comando);
        system(comando);

        strcpy(comando, "./tiny flower_cif.yuv ");
        strcat(comando,aux2);
        strcat(comando," >> resultado.txt");
        printf("O comando ficou assim: %s\n\n\n", comando);
        system(comando); //executa o wine
        sleep(1);
    }

}
