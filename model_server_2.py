# model_server.py
import pickle
import pandas as pd
import cml.models_v1 as models

# Carrega o pipeline 1x por contêiner (pré-processamento + modelo)
with open("pipeline.pkl", "rb") as f:
    PIPELINE = pickle.load(f)

@models.cml_model(metrics=True)  # habilita tracking básico de input/output
def predict(args: dict):
    """
    Espera JSON no formato:
    {"records": { ...campos... }}  ou  {"records": [ {...}, {...} ] }
    Opcional: {"threshold": 0.5}
    Retorna: {"results": [{"churn_probability": float, "prediction": int}, ...]}
    """
    # Normaliza entrada: 1 ou N registros
    data = args.get("records", {})
    rows = data if isinstance(data, list) else [data]
    df = pd.DataFrame(rows).fillna(0)

    # Limite de decisão
    threshold = float(args.get("threshold", 0.5))

    # Predição
    proba = PIPELINE.predict_proba(df)[:, 1].tolist()
    pred = [int(p >= threshold) for p in proba]

    return {
        "results": [
            {"churn_probability": float(p), "prediction": y}
            for p, y in zip(proba, pred)
        ]
    }
