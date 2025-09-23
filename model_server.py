import joblib
import pandas as pd
import cml.models_v1 as models

# Carrega o pipeline treinado
PIPELINE = joblib.load("model.joblib")

@models.cml_model(metrics=True)
def predict(args: dict):
    data = args.get("records", {})
    rows = data if isinstance(data, list) else [data]
    df = pd.DataFrame(rows).fillna(0)

    threshold = float(args.get("threshold", 0.5))
    proba = PIPELINE.predict_proba(df)[:, 1].tolist()
    pred = [int(p >= threshold) for p in proba]

    return {"results": [
        {"churn_probability": float(p), "prediction": y}
        for p, y in zip(proba, pred)
    ]}
