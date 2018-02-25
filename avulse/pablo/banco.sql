-- Criando Tabelas
create table redes(
	id serial primary key,
	nome text,
	jitter decimal(12,8),
	atraso decimal(12,8),
	perda decimal(12,8),
	blur decimal(12,8),
	sinal decimal(12,8)
);

create table log_redes (
    id int,
	nome text,
	jitter decimal(12,8),
	atraso decimal(12,8),
	perda decimal(12,8),
	blur decimal(12,8),
	sinal decimal(12,8)
);

-- Criando função para retirar os dados da tabela redes e colocar na tabela log_redes
CREATE FUNCTION atualizar() RETURNS VOID AS
$$
    insert into  log_redes select * from redes;
    delete from redes;
$$ LANGUAGE 'sql';

-- Exemplo de inserção de dados
-- insert into redes (nome, jitter, atraso, perda, blur) values('GREDES_TESTE', 0.1324, 0.4245, 0.0000, 0.5756);
