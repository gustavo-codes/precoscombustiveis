--Postos
CREATE INDEX idx_postos_cnpj_btree ON postos (cnpj);
CREATE INDEX idx_postos_cidade_estado_btree ON postos (cidade, estado);

CREATE INDEX idx_postos_cnpj_hash ON postos USING hash (cnpj);

--Precos
CREATE INDEX idx_precos_idposto_btree ON precos (id_posto);
CREATE INDEX idx_precos_idcombustivel_btree ON precos (id_combustivel);
CREATE INDEX idx_precos_data_btree ON precos (data_coleta);

CREATE INDEX idx_precos_idposto_hash ON precos USING hash (id_posto);
CREATE INDEX idx_precos_idcombustivel_hash ON precos USING hash (id_combustivel);
