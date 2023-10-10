import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
import numpy as np

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SKETCHY])
server = app.server

# Charger le modèle préalablement exporté
best_model = joblib.load('model.pkl')



data_for_predictions = pd.read_csv('data_for_predictions.csv').set_index('SK_ID_CURR')


# Charger les données de data_affich et data_disply


data_affich = pd.read_csv('df_affich.csv').set_index('SK_ID_CURR')
data_disply = pd.read_csv('data_disply.csv').set_index('SK_ID_CURR')

# Fonction pour effectuer la prédiction
def predict(sk_id_curr):
    # Récupérer les données correspondant à SK_ID_CURR depuis la base de données
    data = data_for_predictions.loc[int(sk_id_curr)]

    # Effectuer la prédiction
    prediction = best_model.predict(data.values.reshape(1, -1))
    probabilities = best_model.predict_proba(data.values.reshape(1, -1))  # Pour obtenir les probabilités des classes

    return prediction[0], probabilities[0]

app.layout = html.Div([
        dbc.Navbar(
    dbc.Container(
        [
            html.Div(html.H4('Prédiction de la Solvabilité du Client'), style = {'color' : 'white'}),
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(dbc.NavbarBrand("Prêt à dépenser", className="ms-2"))
                    ],
                    align="center",
                    className="g-0",
                ),
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="primary",
    dark=True,
    ),
    html.H3('Sélectionnez votre ID Client'),
    dcc.Dropdown(
        id='sk-id-dropdown',
        options=[
            {'label': sk_id, 'value': sk_id} for sk_id in data_for_predictions.index
        ],
    style={'height': '30px', 'width': '150px', 'margin-bottom': '10px'}  
    ),
    html.Button('Prédire', id='predict-button'),

    # Div pour afficher prediction-output
    html.Div(id='prediction-output', className="mb-3"),  # Ajout de la classe "mb-3" pour ajouter un peu d'espace en bas

    # Conteneur pour les deux tableaux

    
    # Div pour afficher table-container
    html.Div([
    html.Div(id='table-container', className="table-responsive")
    ], className="row", style={'margin-left': '5%', 'margin-right': '5%'})
])
#        html.Div([
#        html.Div(id='prediction-output', className="col-3 p-0"),  # Utilisation de la classe "col-6" pour occuper 50% de la largeur
#        html.Div(id='table-container', className="col-6 p-0"),  # Utilisation de la classe "col-6" pour occuper 50% de la largeur
#    ], className="row", style={'margin-left': '0%', 'margin-right': '0%'}),  # Ajout de classes pour créer une grille
#]) 

    
@app.callback(
    [Output('prediction-output', 'children'),
     Output('table-container', 'children')],
    Input('predict-button', 'n_clicks'),
    Input('sk-id-dropdown', 'value')
)
def update_prediction_and_table(n_clicks, sk_id_curr):
    if n_clicks is None or sk_id_curr is None:
        return '', ''

    prediction, probabilities = predict(sk_id_curr)

    # Créer le tableau de prédiction
    prediction_table = html.Div([
        html.H2('Résultat de la prédiction'),
        html.P(f'La prédiction est : {prediction}'),
        html.P('Probabilités :'),
        html.Ul([
            html.Li(f'Classe 0 : {probabilities[0]}'),
            html.Li(f'Classe 1 : {probabilities[1]}')
        ])
    ], style={
    'display': 'flex',        
    'flexDirection': 'column',  
    'alignItems': 'center',       
    'justifyContent': 'center'      
})



    # Créer une liste de noms de colonnes
    names_colonnes = data_affich.columns.tolist()

    # Créer une liste de données
    datas = data_affich.loc[int(sk_id_curr)].tolist()

        # Créer une table pour les données avec une mise en forme personnalisée
    data_affich_table = html.Div([
        html.H2('Données Individus', className='text-center'),
        dbc.Table(
            [
                html.Tr([html.Th('Nom de la Colonne'), html.Th('Valeur')], className="table-info text-center"),  # En-tête avec le thème bleu ciel
                # Boucle pour afficher les noms de colonnes et les valeurs
                *[
                    html.Tr([html.Td(nom, className="text-center"), html.Td(donnee, className="text-center")], className="table-light")
                    for nom, donnee in zip(names_colonnes, datas)
                ],
            ],
            striped=True, bordered=True, hover=True,
        ),
    ],className="table-responsive m-2 col-6") 

    # Ajout d'une classe pour gérer la réactivité de la table si elle est trop grande





    # Créer une liste de noms de colonnes
    noms_colonnes = data_disply.columns.tolist()

    # Créer une liste de données
    donnees = data_disply.loc[int(sk_id_curr)].tolist()

        # Créer une table pour les données avec une mise en forme personnalisée
    data_disply_table = html.Div([
        html.H2('Données Cluster', className='text-center'),
        dbc.Table(
            [
                html.Tr([html.Th('Nom de la Colonne'), html.Th('Valeur')], className="table-info text-center"),  # En-tête avec le thème bleu ciel
                # Boucle pour afficher les noms de colonnes et les valeurs
                *[
                    html.Tr([html.Td(nom, className="text-center"), html.Td(donnee, className="text-center")], className="table-light")
                    for nom, donnee in zip(noms_colonnes, donnees)
                ],
            ],
            striped=True, bordered=True, hover=True,
        ),
    ], className="table-responsive m-2 col-6")  # Ajout d'une classe pour gérer la réactivité de la table si elle est trop grande


    # Conteneur pour les deux tables sur la même ligne
    tables_container = html.Div([data_affich_table, data_disply_table], className="d-flex")


  

  

    return prediction_table, tables_container
    #[data_affich_table, html.Br(), data_disply_table]

if __name__ == '__main__':
    app.run_server(debug=True)
