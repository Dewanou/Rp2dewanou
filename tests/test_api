import requests

# URL de votre API FastAPI
api_url = "https://lgbpdcapi-ce5a61ec45e8.herokuapp.com/predict/"

# ID du client que vous souhaitez tester
sk_id_curr = 100013  

# Créez la requête GET avec l'ID du client
response = requests.get(api_url + str(sk_id_curr))

# Vérifiez le code de réponse HTTP
if response.status_code == 200:
    data = response.json()
    prediction = data.get("prediction", "N/A")
    probabilities = data.get("probabilities", [0, 0])  # Mettez une valeur par défaut pour les probabilités

    print(f"ID du client : {sk_id_curr}")
    print(f"Prédiction : {prediction}")
    print(f"Probabilité d'obtenir le crédit : {round(probabilities[0]*100, 2)} %")
    print(f"Probabilité de refus : {round(probabilities[1]*100, 2)} %")
else:
    print(f"Erreur - Code de réponse HTTP : {response.status_code}")
