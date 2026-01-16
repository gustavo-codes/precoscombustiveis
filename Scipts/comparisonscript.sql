SET enable_indexscan = off;
SET enable_bitmapscan = off;
SET enable_indexonlyscan = off;
SET enable_hashjoin = off;
SET enable_mergejoin = off;
SET enable_nestloop = on;

RESET enable_indexscan;
RESET enable_bitmapscan;
RESET enable_indexonlyscan;
RESET enable_hashjoin;
RESET enable_mergejoin;
RESET enable_nestloop;




EXPLAIN ANALYZE
WITH precos_por_mes AS (
    SELECT 
        postos.estado,
        EXTRACT(MONTH FROM precos.data_coleta) AS mes,
        AVG(precos.preco) AS preco_medio
    FROM precos
    JOIN postos USING(id_posto)
    JOIN combustiveis USING(id_combustivel)
    WHERE combustiveis.id_combustivel = 10
      AND precos.data_coleta BETWEEN '2025-01-01' AND '2025-12-31'
    GROUP BY postos.estado, EXTRACT(MONTH FROM precos.data_coleta)
)
SELECT
    jan.estado,
    jan.preco_medio AS preco_janeiro,
    jun.preco_medio AS preco_junho,
    (jun.preco_medio - jan.preco_medio) AS variacao_absoluta,
    ROUND(((jun.preco_medio - jan.preco_medio) / jan.preco_medio) * 100, 2) AS variacao_percentual
FROM precos_por_mes jan
JOIN precos_por_mes jun 
    ON jan.estado = jun.estado
WHERE jan.mes = 1
  AND jun.mes = 6
ORDER BY jan.estado;

