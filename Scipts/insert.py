import pandas as pd
from sqlalchemy.exc import IntegrityError
from database import SessionLocal
from models import Posto, Combustivel, Preco

CSV_PATH = "../Data/2005.csv"
DELIMITER = ";"
BATCH_SIZE = 5000

df = pd.read_csv(CSV_PATH, sep=DELIMITER, encoding="latin1", low_memory=False)

df.columns = [
    "regiao", "estado", "cidade", "razao_social", "cnpj",
    "endereco", "numero", "nome_fantasia", "bairro", "cep",
    "produto", "data_coleta", "preco", "unidade", "bandeira", "valor_ref"
]

df["data_coleta"] = pd.to_datetime(
    df["data_coleta"], dayfirst=True, errors="coerce"
).dt.date

df["preco"] = (
    df["preco"].astype(str)
    .str.replace(",", ".", regex=False)
    .str.replace(r"[^\d.]", "", regex=True)
    .astype(float)
)

df["cnpj"] = (
    df["cnpj"].astype(str)
    .str.replace(r"\D", "", regex=True)
    .str.zfill(14)
)

df = df[
    (df["cnpj"].str.len() == 14) &
    (df["preco"].notna()) &
    (df["data_coleta"].notna())
]

session = SessionLocal()
postos_cache = {}
combustiveis_cache = {}
precos_to_insert = []

for _, row in df.iterrows():
    cnpj = row["cnpj"]
    if cnpj in postos_cache:
        posto = postos_cache[cnpj]
    else:
        posto = session.query(Posto).filter_by(cnpj=cnpj).first()
        if not posto:
            posto = Posto(
                cnpj=cnpj,
                razao_social=str(row["razao_social"] or "")[:255],
                nome_fantasia=str(row["nome_fantasia"] or "")[:255],
                bandeira=str(row["bandeira"] or "")[:50],
                endereco=str(row["endereco"] or "")[:255],
                numero=str(row["numero"] if pd.notna(row["numero"]) else "")[:20],
                bairro=str(row["bairro"] or "")[:100],
                cep=str(row["cep"] or "")[:20],
                cidade=str(row["cidade"] or "")[:100],
                estado=str(row["estado"] or "")[:10],
                regiao=str(row["regiao"] or "")[:20]
            )
            session.add(posto)
            session.flush()
        postos_cache[cnpj] = posto


    produto = row["produto"]
    if produto in combustiveis_cache:
        combustivel = combustiveis_cache[produto]
    else:
        combustivel = session.query(Combustivel).filter_by(descricao=produto).first()
        if not combustivel:
            combustivel = Combustivel(
                descricao=str(produto or "")[:255],
                unidade_medida=str(row["unidade"] or "")[:20]
            )
            session.add(combustivel)
            session.flush()
        combustiveis_cache[produto] = combustivel


    preco = Preco(
        id_posto=posto.id_posto,
        id_combustivel=combustivel.id_combustivel,
        data_coleta=row["data_coleta"],
        preco=row["preco"]
    )
    precos_to_insert.append(preco)

    if len(precos_to_insert) >= BATCH_SIZE:
        try:
            session.bulk_save_objects(precos_to_insert)
            session.commit()
        except IntegrityError:
            session.rollback()
        precos_to_insert = []


if precos_to_insert:
    try:
        session.bulk_save_objects(precos_to_insert)
        session.commit()
    except IntegrityError:
        session.rollback()

session.close()
print("Carga finalizada com sucesso!")
