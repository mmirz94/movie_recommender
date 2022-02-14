from defaults import *

app = dash.Dash(__name__, title= 'Movie Recommender', update_title=None, external_stylesheets=[dbc.themes.BOOTSTRAP], assets_folder = 'assets')
server = app.server

content_based_app_layout = html.Div(
    [
        html.Div(style={'height':'1rem'}),
        html.Div(
            [
                html.Div(
                    dcc.Dropdown(
                        list(movies['title'].values),
                        id='movie_name',
                        placeholder="Select a movie that you like",
                        style={'width':'99.5%'}
                    ),
                    style={'width':'35%', 'display':'inline-block', 'verticalAlign': 'middle'}
                ),
                html.Div(
                    dcc.Dropdown(
                        [1,2,3,4,5,6,7,8,9,10],
                        id='num_recommendations',
                        placeholder="How many recommendation would you like to see?",
                        # multi=True,
                        style={ 'width':'99.5%'}
                    ),
                    style={'width':'35%','display':'inline-block', 'verticalAlign': 'middle'}
                ),
                html.Div(
                    dbc.Button("Go!", id ='go_button' ,color="primary", style={'width':'50px'}),
                    style={'width':'15%', 'display':'inline-block', 'verticalAlign': 'middle'}
                )
            ],
            style={'margin-left':'1rem'}
        ),
        html.Div(
                    [
                        default_recommended_movies_table
                    ],
                    id='table_container',
                    style={'display':'none'}
                    ),
    ],
    style={'background-image': 'url(assets/background_img.jpg)',
           'height':'100vh', 'width':'100%', 'background-size': 'cover'},
)


app.layout = content_based_app_layout

@app.callback(
    [
        Output('table_container', 'style'),
        Output('recommended_movies_table', 'data')
    ],
    [
        Input("go_button","n_clicks")
    ],
    [
        State('movie_name', 'value'),
        State('num_recommendations', 'value')
    ],
    prevent_initial_call=True
)
def get_recommendations(n_click, movie_name, num_recommendations):
    table_data = content_based_recommender(movie_name, movies, cosine_sim, num_recommendations)
    return {'width':'90%',  'margin-right': 'auto', 'margin-left': 'auto', 'margin-top':'1rem'}, table_data



if __name__ == '__main__':
    app.run_server(host='localhost', debug=True, dev_tools_hot_reload=False, port=8000)
