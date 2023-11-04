import dash
import requests
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objs as go

# Charger les données de data_affich, data_disply, new_row_0, new_row_1, feature_importance_df (remplacez les noms de fichiers par les vôtres)
data_display = pd.read_csv('data_display.csv').set_index('SK_ID_CURR')
new_row_0 = pd.read_csv('new_row_0.csv')
new_row_1 = pd.read_csv('new_row_1.csv')
feature_importance_df = pd.read_csv('feature_importance_df.csv')

# Variables à comparer
variables = ['Montant_credit', 'Densité_relative_population', 'Age', 'Anciennete', 'Nb_de_titres_actifs', 'Nb_Remboursement', 'Revenu_par_tête']

# Variables qualitatives à comparer
variables_qualitatives = ['Genre', 'Type_de_revenu', 'Niveau_education', 'Statut_familial', 'Type_de_logement']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUMEN])

server = app.server

# Layout de la page 1
layout_page_1 = html.Div([
    dbc.Navbar(
        dbc.Container(
            [
                html.Div(html.H4('Prédiction de la Solvabilité du Client'), style={'color': 'white'}),
                html.A(
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
            {'label': str(sk_id), 'value': sk_id} for sk_id in data_display.index
        ],
        style={'height': '30px', 'width': '150px', 'margin-bottom': '10px'}
    ),
    html.Button('Prédire', id='predict-button'),

    # Div pour afficher prediction-output
    html.Div(id='prediction-output', className="mb-3"),  # Ajout de la classe "mb-3" pour ajouter un peu d'espace en bas

    # Div pour afficher les données du client sélectionné
    html.H3('Données du client sélectionné', style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center'
    }),
    html.Div(id='selected-client-data', style={'margin': '0', 'padding': '0', 'border': 'none'}),  # Réduire la marge et enlever le cadre du tableau
])

# Callback de la page 1
@app.callback(
    [Output('prediction-output', 'children'),
     Output('selected-client-data', 'children')],
    [Input('predict-button', 'n_clicks'),
     Input('sk-id-dropdown', 'value')]
)
def update_prediction_and_table(n_clicks, sk_id_curr):
    if n_clicks is None or sk_id_curr is None:
        return '', ''

    # Faites une requête GET à votre API FastAPI en utilisant l'URL appropriée
    api_url = f"http://localhost:8000/predict/{sk_id_curr}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        prediction = data.get("prediction", "N/A")
        probabilities = data.get("probabilities", [0, 0])  # Mettez une valeur par défaut pour les probabilités
    else:
        prediction = "Erreur"
        probabilities = [0, 0]  # Mettez une valeur par défaut pour les probabilités

    # Créez le tableau de prédiction
    if prediction == 0:
        prediction_text = "Accord"
    elif prediction == 1:
        prediction_text = "Refus"
    else:
        prediction_text = "N/A"

    prediction_table = html.Div([
        html.H2("Suite à l'analyse des données clients"),
        html.P(f'La décision est : {prediction_text}'),  # Utilisez prediction_text
        html.P('Probabilités :'),
        html.Ul([ 
            html.Li(f"Probabilité du client d'obtenir le crédit : {round(probabilities[0]*100, 2)} %"),
            html.Li(f"Probabilité du client d'avoir un refus : {round(probabilities[1]*100, 2)} %")
        ])
    ], style={
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'center'
    })

    # Obtenez les données du client sélectionné
    selected_client_data = data_display.loc[sk_id_curr]

    # Créez un tableau HTML pour afficher les données du client
    selected_client_data_table = dbc.Table(
        [
            html.Tr([html.Th('Nom de la Colonne'), html.Th('Valeur')], className="table-info text-center"),
            *[
                html.Tr([html.Td(nom, className="text-center"), html.Td(donnee, className="text-center")], className="table-light")
                for nom, donnee in zip(selected_client_data.index, selected_client_data.values)
            ],
        ],
        striped=True, bordered=True, hover=True,
        className="table-responsive m-2 col-6"
    )

    return prediction_table, selected_client_data_table

# Layout de la page 2
layout_page_2 = html.Div([
    dcc.Dropdown(
        id='variable-dropdown',
        options=[
            {'label': variable, 'value': variable} for variable in variables
        ],
        value='Montant_credit'
    ),
    dcc.Graph(id='scatter-3d'),
    dcc.Dropdown(
        id='variable-dropdown-qualitative',
        options=[
            {'label': variable, 'value': variable} for variable in variables_qualitatives
        ],
        value='Genre'
    ),
    html.Div(id='data-table')
])

# Callback de la page 2
@app.callback(
    [Output('scatter-3d', 'figure'),
     Output('data-table', 'children')],
    [Input('variable-dropdown', 'value'),
     Input('variable-dropdown-qualitative', 'value')]
)
def update_graph_and_table(selected_variable, selected_variable_qualitative):
    values_1 = new_row_1[selected_variable].values[0]
    values_0 = new_row_0[selected_variable].values[0]
    
    trace1 = go.Bar(x=['Classe 1'], y=[values_1], name='Classe 1')
    trace2 = go.Bar(x=['Classe 0'], y=[values_0], name='Classe 0')
    
    data = [trace1, trace2]
    
    layout = go.Layout(
        title=f'Comparaison de {selected_variable} entre Classe 1 (Refus) et Classe 0 (Accord)',
        scene=dict(
            xaxis=dict(title='Classe'),
            yaxis=dict(title=selected_variable),
        )
    )
    
    fig = go.Figure(data=data, layout=layout)

    if selected_variable_qualitative:
        selected_data_1 = new_row_1[[selected_variable_qualitative]]
        selected_data_2 = new_row_0[[selected_variable_qualitative]]
        
        table_data_1 = html.Div([
            html.H3('Données pour Individu moyen à qui on a refusé le crédit', style={'text-align': 'left'}),
            generate_table(selected_data_1, center=False)
        ], style={'text-align': 'left'})  # Ajouter la classe CSS pour centrer
        
        table_data_2 = html.Div([
            html.H3('Données pour Individu moyen à qui on a accordé le crédit', style={'text-align': 'left'}),
            generate_table(selected_data_2, center=False)
        ], style={'text-align': 'left'})  # Ajouter la classe CSS pour centrer

        return fig, [table_data_1, table_data_2]

    return fig, ''

# Générer le tableau HTML (page 2)
def generate_table(dataframe, max_rows=10, center=False):
    style = {'text-align': 'center'} if center else {}  # Style pour centrer le texte
    return html.Table(
        # En-têtes de tableau
        [html.Tr([html.Th(col, style=style) for col in dataframe.columns])] +

        # Lignes de données
        [html.Tr([html.Td(dataframe.iloc[i][col], style=style) for col in dataframe.columns]) for i in range(min(len(dataframe), max_rows))])

# Créez la figure avec la trace du diagramme en radar (page 3)
feature_importance_data = feature_importance_df.set_index('Feature').head(10)

trace = go.Scatterpolar(
    r=feature_importance_data.values.flatten(),
    theta=feature_importance_data.index,
    fill='toself',
    name='Feature Importance'
)

# Personnalisez la mise en page du graphique (page 3)
fig = go.Figure(trace)
fig.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
        ),
    ),
    showlegend=False,
    title='Top 10 Features Importance Radar Chart'
)

# Layout de la page 3
layout_page_3 = html.Div([
    dcc.Graph(figure=fig)
])

# Layout de l'application avec les onglets
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Page 1', children=layout_page_1),
        dcc.Tab(label='Page 2', children=layout_page_2),
        dcc.Tab(label='Page 3', children=layout_page_3)
    ])
])

if __name__ == '__main__':
    app.run_server(debug=True)
