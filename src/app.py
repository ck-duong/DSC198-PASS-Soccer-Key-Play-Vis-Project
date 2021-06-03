import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np

import src.viz as viz
import src.tracking as track

#####

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

games = ['Humboldt', 'Point Loma', 'Pomona', 'Sonoma']

#####

game_frames = track.read_all_games()
game_zero = game_frames[0]
players = set()

for i in game_frames:
    game_players = i['Player'].unique()
    players.update(game_players)
players = list(players)



app.layout = html.Div([
    html.Div([
        html.Label('Game Dropdown'),
        dcc.Dropdown(
            id = 'game-name',
            options = [
                {'label': game, 'value': game for game in games}
            ]
    ),
        html.Label('Player Dropdown'),
        dcc.Dropdown(
            id = 'player-name',
            options = [
                {'label': player, 'value': player for player in players}
            ]
    )
    ]),
    
    html.Div([
        children = [
            html.H1(children = 'Heat maps'),

            html.Div(children = '''
            Soccer Player heatmap mapping application
            '''),

            dcc.Graph(
            id = 'heatmap')
        ]
    ])
    
])
    
@app.callback(
dash.dependencies.Output('heatmap', 'figure'),
    [dash.dependencies.Input('game-name', 'value'),
    dash.dependencies.Input('player-name', 'value')]
)

def update_graph(game_name, player_name):
    dff = game_frames[games.index(game_name)]
    
    coord_df = track.get_player_coordinates(dff, 'Latitude', 'Longitude')

    dff['Converted Latitude'] = coord_df.apply(lambda x: x[0] + 51.5)
    dff['Converted Longitude'] = coord_df.apply(lambda y: y[1] + 33)

    df = dff[['Player', 'Seconds', 'Converted Latitude', 'Converted Longitude']]

    df['Converted Latitude'] = df['Converted Latitude'].apply(lambda x: x if (x >= 0) & (x <= 103) else np.nan)
    df['Converted Longitude'] = df['Converted Longitude'].apply(lambda x: x if (x >= 0) & (x <= 66) else np.nan)
    
    fig = make_heat_map(df, player_name, 'Converted Latitude',
              'Converted Longitude')
    
    return fig
######

if __name__ == '__main__':
    app.run_server(debug=True)