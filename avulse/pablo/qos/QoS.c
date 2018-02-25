#include<stdio.h>
#include<stdlib.h>
#include<string.h>
/*
    Autor: Fábio Lima da Silva
    Programa de QoS que calcula jitter, perda e atraso
    Deve ser executado com root e usar parâmetros
    Ex:
    ./QoS 1.1.1.2 600 30
    Parâmetro 1 : Nome do Programa
    Parâmetro 2 : IP que deseja fazer os pings
    Parâmetro 3 : Quantidade de amostras que deseja fazer
    Parâmetro 4 : Quantidade de ping que cada amostra irá ter
*/

int verify_user() {
    /* Verifica se o usuário é root, se não for, termina programa */
    FILE *user;
    system("whoami > usuario");
    user = fopen("usuario", "r");
    char usuario[15];
    fscanf(user, " %[^\n]", usuario);
    fclose(user);
    if (strcmp(usuario, "root") != 0) {
        printf("Precisa ser root!\n");
        return 0;
    } else {
        system("rm usuario");
        return 1;
    }
}


/* Função Jitter ------------------------------------------------------ */
float jitter(float *vetor, int qtd) {
    float jitter = 0, somajitter = 0, jitter_final = 0;
    int i;
    for (i = 1; i < qtd; i++) {
        jitter = (vetor[i] - vetor[i - 1])/2;
        if (jitter < 0)//se o valor do jitter for negativo ele transforma em positivo
            jitter = jitter * (-1);
        somajitter += jitter;
    }
    jitter_final = somajitter / qtd;
    return jitter_final;
}

/* Função Atraso ------------------------------------------------------ */
float atraso(float *vetor, int qtd) {
    int i;
    float delay = 0;
    for (i = 0; i < (qtd); i++) {
        delay = delay + (vetor[i] / 2);
    }
    delay = delay / (qtd);
    return delay;
}

main(int argc, char ** argv) {
    system("clear");
    if (argc != 4) {
        printf("Insira os parametros corretamente\n");
        printf("Use: ./QoS [IP] [Qtd amostra] [Qtd ping]\n");
        exit(0);
    }
    
    /* Verifica se o usuário é root, se não for, termina programa */
    int user = verify_user();
    if (user == 0) {
        exit(0);
    }
    
    /* Funções utilizadas para contar a duração do programa */
    float tempo_proc;
    struct timeval *calc_limiar;
    calc_limiar = (struct timeval*) malloc(sizeof (struct timeval)); //atribuir memoria a struct de ponteiro criada
    gettimeofday(&calc_limiar[0], NULL);

    /* --------------------------------------------------------------- */
    FILE *arq;
    FILE *dados;
    char ip[15], comando[100];
    int repeat = atoi(argv[2]);
    char qtd_ping[6];    
    int z;
    int tempos = 0, i;
    float value, delay = 0,value_max = -1, perda = 0;
    float atraso_total = 0;
    float jitter_total = 0, j = 0;
    float perda_total = 0;
    strcpy(qtd_ping, argv[3]);
    int qtdping = atoi(qtd_ping);
    strcpy(ip, argv[1]); //coloca o IP informado no parâmetro e coloca dentro da variável
    strcpy(comando, "ping -c ");
    strcat(comando, qtd_ping);
    strcat(comando, " -i 0 ");
    strcat(comando, ip);
    strcat(comando, " | grep ttl| cut -d '=' -f4| cut -d ' ' -f1 > ping");
    printf("Calculando QoS\nAguarde...\n\n");
    dados = fopen("resultados","w");
    for (z = 0; z < repeat; z++) {
        /* Coleta------------------------------------------------------ */
        system(comando);
        arq = fopen("ping", "r+");
        while (!feof(arq)) {
            if (fgetc(arq) == '\n') //se encontrar \n no arquivo, incrementa o valor de tempo
                tempos++; //conta quantos pings existem no arquivo
        }
        float valores[tempos];
        rewind(arq); //coloca o ponteiro do arquivo no inicio
        for (i = 0; !feof(arq); i++) {
            fscanf(arq, "%f", &value); //pega os valores do arquivo
            valores[i] = value; //coloca os valores no vetor
        }
        /* ------------------------------------------------------------ */
        j = jitter(valores, tempos);
        jitter_total += j;
        /* ------------------------------------------------------------ */
        perda = qtdping - tempos;
        perda_total += perda;
        /* ------------------------------------------------------------ */
        delay =  atraso(valores, tempos);
        atraso_total += delay;
        /* ------------------------------------------------------------ */
        system("rm ping");        
        fclose(arq);
        fprintf(dados,"%.3f\t",j);
		fprintf(dados,"%.3f\t",delay);
		fprintf(dados,"%f\t",perda/tempos);
		fprintf(dados,"%.3f\t",j+0.005);
		fprintf(dados,"%.3f\t",j-0.005);
		fprintf(dados,"%.3f\t",delay+0.005);
		fprintf(dados,"%.3f\n",delay-0.005);
		if(j > delay && delay >= value_max){
		    value_max = j;
		} else if(delay > j && j >= value_max){
		    value_max = delay;
		}
		tempos = 0;
    }
        fclose(dados);
        system("cat -n resultados| awk '{print $1, $2, $3, $4, $5, $6, $7, $8}' > result");
	    system("rm resultados");
        
        jitter_total = jitter_total / repeat;
        perda_total /= repeat;
        atraso_total /= repeat;
        
        printf("Média do Jitter -> %.3f\n",jitter_total);
        printf("Média do  Atraso -> %.3f\n",atraso_total);
        printf("Média da Perda  -> %.3f\n",perda_total);
        
        printf("Maior valor encontrado: %.3f\n",value_max);
        
    /* Funções utilizadas para contar a duração do programa */
    gettimeofday(&calc_limiar[1], NULL);
    tempo_proc = (((calc_limiar[1].tv_sec - calc_limiar[0].tv_sec)*1000.0) + (calc_limiar[1].tv_usec - calc_limiar[0].tv_usec) / 1000.0) / 1000.0;
    printf("\nTempo de processamento: %.2f segundos\n", tempo_proc);
    /* --------------------------------------------------------------- */
}
