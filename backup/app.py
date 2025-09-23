# app.py
import pickle
from typing import List, Union, Optional
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

# ===== Carrega o pipeline treinado (preprocessamento + modelo) =====
# Certifique-se de que pipeline.pkl está na mesma pasta.
with open("pipeline.pkl", "rb") as f:
    pipeline = pickle.load(f)

# ===== Schemas de entrada/saída =====
class Customer(BaseModel):
    idade: Optional[float] = Field(None, ge=0)
    genero: Optional[str] = Field(None, description="Ex.: 'M' ou 'F'")
    tempo_de_contrato_meses: Optional[float] = Field(None, ge=0)
    gasto_mensal: Optional[float] = Field(None, ge=0)

class PredictRequest(BaseModel):
    records: Union[Customer, List[Customer]]

class PredictResponseItem(BaseModel):
    churn_probability: float
    prediction: int

app = FastAPI(
    title="Churn API (FastAPI + scikit-learn Pipeline)",
    version="1.0.0",
    description="Serviço de predição de churn utilizando um Pipeline do scikit-learn."
)

# ===== Healthcheck =====
@app.get("/health")
def health():
    return {"status": "ok"}

# ===== Predição =====
@app.post("/predict", response_model=List[PredictResponseItem])
def predict(payload: PredictRequest, threshold: float = Query(0.5, ge=0.0, le=1.0)):
    """
    Recebe 1 ou N registros em `records` e retorna probabilidade de churn e classe prevista.
    Param opcional `threshold` define o corte (default 0.5).
    """
    try:
        # Normaliza para lista
        records = payload.records if isinstance(payload.records, list) else [payload.records]

        # Converte para DataFrame e trata ausências com 0 (ajuste se preferir uma estratégia diferente)
        df_in = pd.DataFrame([r.dict() for r in records]).fillna(0)

        # Usa o pipeline completo (preprocess + modelo)
        proba = pipeline.predict_proba(df_in)[:, 1].tolist()
        pred = [int(p >= threshold) for p in proba]

        return [
            PredictResponseItem(churn_probability=float(p), prediction=cls)
            for p, cls in zip(proba, pred)
        ]
    except Exception as e:
        # Erros de schema/colunas inesperadas ou inconsistências de treino
        raise HTTPException(status_code=400, detail=f"Prediction error: {e}")

#Para rodar no terminal
#uvicorn app:app --host 0.0.0.0 --port 5000 --workers 2