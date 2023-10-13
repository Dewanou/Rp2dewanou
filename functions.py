
import pandas as pd
import joblib
import numpy as np


# Charger le modèle préalablement exporté
best_model = joblib.load('model.pkl')



data_for_predictions = pd.read_csv('data_for_predictions.csv').set_index('SK_ID_CURR')


def predict(sk_id_curr):
    # Récupérer les données correspondant à SK_ID_CURR depuis la base de données
    data = data_for_predictions.loc[int(sk_id_curr)]

    # Effectuer la prédiction
    prediction = best_model.predict(data.values.reshape(1, -1))
    probabilities = best_model.predict_proba(data.values.reshape(1, -1))  # Pour obtenir les probabilités des classes

    return prediction[0], probabilities[0]


