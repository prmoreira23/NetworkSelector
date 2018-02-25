#include<stdio.h>
#include<stdlib.h>
#include<string.h>

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
    /* --------------------------------------------------------------- */
    FILE *arq;
    FILE *dados;
    int tempos = 0, i;
    float value, delay = 0, perda = 0;
    float j = 0;
    int l=0;

    printf("Calculando QoS\nAguarde...\n\n");
    system("cat arq | awk '{print $3}'| cut -d= -f2 > ping");
    arq = fopen("ping", "r");
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
    /* ------------------------------------------------------------ */
    delay = atraso(valores, tempos);
    /* ------------------------------------------------------------ */
    fclose(arq);
    system("rm ping");
    system("tail -n 1 arq | cut -d' ' -f1 > qtd");
    arq = fopen("qtd","r");
    fscanf(arq, "%d", &l);
    fclose(arq);
    dados = fopen("resultado_qos","a");
    fprintf(dados, "%.3f\t", j);
    fprintf(dados, "%.3f\t", delay);
    fprintf(dados, "%d\n", l - tempos);
    fclose(dados);
    system("rm qtd");
}
