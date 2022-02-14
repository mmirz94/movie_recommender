import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import os
import pathlib
from dash.dash import no_update
from dash import dash_table
from dash.dash_table.Format import Format, Group
import numpy as np
import pandas as pd
import json

PATH = pathlib.Path(__file__).parent
PATH_DATA=os.path.join(PATH,"assets")

movies = pd.read_csv(os.path.join(PATH_DATA,'movies_and_indices.csv'))
cosine_sim = np.load(os.path.join(PATH_DATA, 'cosine_sim_matrix.npz'))['cosine_sim']

colors = {'heading':'#ed1f1f', 'text':'#ffffff'}

Recommended_movies_table_columns=['Movie Title', 'Genres', 'Cast', 'Overview']
default_recommended_movies_table= dash_table.DataTable(
                    id='recommended_movies_table',
                    columns = [{"name": i, "id": i} for i in Recommended_movies_table_columns],
                    row_deletable=False,
                    style_table={'height': '90%', 'overflowY': 'auto'},
                    style_header={'backgroundColor': colors['heading'], 'fontWeight': 'bold', 'font_family': 'cursive','font_size': '17px', 'text-align': 'left', 'color':colors['text'], 'margin-left':'0px'},
                    style_data={'font_family': 'cursive', 'font_size': '14px', 'textAlign': 'left', 'color':'#111111', 'whiteSpace': 'normal', 'height': 'auto',},

                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220,224,230)'
                        },

                    ],
                    )


MF_Recommended_movies_table_columns=['Movie Title', '% Match']
default_MF_recommended_movies_table= dash_table.DataTable(
                    id='MF_recommended_movies_table',
                    columns = [{"name": i, "id": i} for i in MF_Recommended_movies_table_columns],
                    row_deletable=False,
                    style_table={'height': '90%', 'overflowY': 'auto'},
                    style_header={'backgroundColor': colors['heading'], 'fontWeight': 'bold', 'font_family': 'cursive','font_size': '17px', 'text-align': 'left', 'color':colors['text'], 'margin-left':'0px'},
                    style_data={'font_family': 'cursive', 'font_size': '14px', 'textAlign': 'left', 'color':'#111111', 'whiteSpace': 'normal', 'height': 'auto',},

                    style_data_conditional=[
                        {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(220,224,230)'
                        },

                    ],
                    )


def content_based_recommender(title, movies, cosine_sim, top_x_movies):
    # Get the index of the movie that matches the title
    indices_series = pd.Series(movies['index'])
    indices_series.index = movies['title']
    idx = indices_series[title]

    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))  # add a counter to an iterable

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_x_movies+1]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = pd.DataFrame(movies.iloc[movie_indices])
    recommended_movies = recommended_movies[['title', 'genres', 'cast', 'overview']]
    recommended_movies.columns = ['Movie Title', 'Genres', 'Cast', 'Overview']  #column names should match those in the dash table

    return recommended_movies.to_dict('records')

