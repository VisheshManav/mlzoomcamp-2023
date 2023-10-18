import pickle
from flask import Flask
from flask import request, jsonify

with open("model1.bin", "rb") as m_in:
  model = pickle.load(m_in)
with open("dv.bin", "rb") as dv_in:
  dv = pickle.load(dv_in)

app = Flask("credit")

@app.route("/predict", methods=["POST"])
def predict():
  client = request.get_json()

  X = dv.transform([client])
  y_pred = model.predict_proba(X)[:, 1]
  prob = y_pred[0]
  credit = prob >= 0.5

  response = {
    "credit-probability": float(prob),
    "credit": bool(credit)
  }

  return jsonify(response)


if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port="9696")