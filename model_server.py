import cml.models_v1 as models

@models.cml_model(metrics=True)
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
