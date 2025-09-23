from joblib import load

model = load('model.joblib')

@models.cml_model
def predict(args):
  dep_delay = args["dep_delay"]
  prediction = model.predict([[dep_delay]]).item()
  return {"pred_arr_delay": round(prediction)}