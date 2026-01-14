CREATE TABLE postos (
    id_posto        SERIAL PRIMARY KEY,
    cnpj            VARCHAR(18) NOT NULL,
    razao_social    VARCHAR(255) NOT NULL,
    nome_fantasia   VARCHAR(255),
    bandeira        VARCHAR(50),
    endereco        VARCHAR(255) NOT NULL,
    numero          VARCHAR(20),
    bairro          VARCHAR(100),
    cep             VARCHAR(10),
    cidade          VARCHAR(100) NOT NULL,
    estado          CHAR(2) NOT NULL,
    regiao          VARCHAR(20)
);

CREATE TABLE combustiveis (
    id_combustivel  SERIAL PRIMARY KEY,
    descricao       VARCHAR(50) NOT NULL,
    unidade_medida  VARCHAR(10) NOT NULL
);

CREATE TABLE precos (
    id_preco        SERIAL PRIMARY KEY,
    id_posto        INTEGER NOT NULL,
    id_combustivel  INTEGER NOT NULL,
    data_coleta     DATE NOT NULL,
    preco           NUMERIC(10,2) NOT NULL,
    moeda           CHAR(2) DEFAULT 'R$',

    CONSTRAINT fk_precos_posto
        FOREIGN KEY (id_posto)
        REFERENCES postos (id_posto)
        ON DELETE CASCADE,

    CONSTRAINT fk_precos_combustivel
        FOREIGN KEY (id_combustivel)
        REFERENCES combustiveis (id_combustivel)
        ON DELETE RESTRICT
);
