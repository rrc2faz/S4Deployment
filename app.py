# Import dependencies 
import seaborn as sns
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
from plotly.graph_objs import Layout
from plotly.offline import init_notebook_mode, iplot, plot
import matplotlib.pyplot as plt
import dash_bootstrap_components as dbc

# import data
df = pd.read_csv("data.csv")

# Make new dataframe
list = ['Christopher Nolan', 'Martin Scorsese', 'Steven Spielberg', 'Quentin Tarantino','Tim Burton','Kathryn Bigelow','James Cameron','Spike Lee','Greta Gerwig', 'David Fincher']
df_Directors = df[df.Director.isin(list)]

# Define layout and elements
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR, dbc_css]) # initialize the app
#app = dash.Dash(external_stylesheets=[dbc.themes.CYBORG])

# Create min and max release year for later
min_date = df_Directors['Release Year'].min()  # get the minimum value of year in the dataset
max_date = df_Directors['Release Year'].max()  # maximum value of year

# Begin app creation 
app.layout = dbc.Container([
    html.Br(),  # Breaks for formatting
    html.Br(),
    html.Div(children = [   # Text at top of page
        dcc.Markdown(
            '''# Cinemaniac ''', 
        ),
        dcc.Markdown(
            '''##### Welcome to Cinemaniac! Use the interactive graph below to dive into our database and uncover trends, statistics, and insights into the top directors in the film industry. Whether you're a movie buff, industry professional, or simply curious about cinema, Cinemaniac offers a dynamic app to enrich your movie experience. ''', 
            style = {'color': 'rgba(226,217,243,255)'}
        ),
    ], className = 'dbc' ),
    html.Br(),
    html.Div(children = [   # Dropdown 
                html.Label('Select Director'),
        dcc.Dropdown(
            options = [{'label':director, 'value':director} for director in df_Directors['Director']],  # Options are all directors in dataset
            value = [],   # Making the default value an empty list  
            multi = True,    # Can select more than one director
            id = 'director_dropdown',  
            )
    ], style = {'width':'50%', 'display':'inline-block'}, className = 'dbc'),
    html.Div(children = [   # Slider 
        html.Label('Select Release Date Range'),    # Label for slider 
        dcc.RangeSlider( 
            min = min_date,
            max = max_date,
            value = [min_date, max_date],   # Make default value the whole range of years in dataset
            step = 1,    # Can go up/down by 1 
            marks = None,   # I don't want marks
            id = 'range_slider',
            tooltip={"placement": "bottom", "always_visible": True},
            allowCross = False,     # Prevent slider points from crossing over each other 
        )
    ], style = {'width':'50%', 'display':'inline-block'}, className = 'dbc'),  # Take up half of screen 
    html.Br(),
    html.Br(),
    html.Div(children = [   # Graph, so it knows when to place it 
        dcc.Graph(
            id='indicator_graph',
        ), ],
        className = 'twelve columns'),   # Take up whole screen 
    ], className = 'dbc')   # Placement along row 

# Every function must have its own callback operator
@callback(
    Output('indicator_graph', 'figure', allow_duplicate=True),   # Outputs
    Input('director_dropdown', 'value'),   # Dropdown input 
    Input('range_slider', 'value'),   # Slider input 
    prevent_initial_call=True)   # May not need this, but fixed an error at one point 

def update_graph(selected_director, year_range):   # update graph function 

    choices = df_Directors[df_Directors['Director'].isin(selected_director)]
    choices = choices[choices['Release Year'].astype(int).between(year_range[0], year_range[1])]

    fig = px.scatter(
        choices,  # user inputs 
        x="Gross worldwide (in millions)",   # xaxis value
        y="Rating (Out of 10)",   # yaxis value
        size="Budget (in millions)",   # size of bubble plots points
        color='Director',  # color points by director name
        hover_name='Title',   # Make sure the title of the film appears when hovering over point
        opacity = 0.9   # High opacity so it's bright against dark background
        #color_discrete_sequence = 'Light24',
        #legend='full', 
    )

    fig.update_layout(
        paper_bgcolor = 'rgba(37,13,73,255)',   # Change background color
        plot_bgcolor = 'rgba(37,13,73,255)',
        xaxis_gridcolor = 'rgba(37,13,73,255)',   # Make grids disappear against color
        yaxis_gridcolor = 'rgba(37,13,73,255)',
        font = dict(
            color = 'rgba(226,217,243,255)',
        )
    )

    fig.update_xaxes(
        showgrid=False,   # No grid 
        showline = True,   # Still want line at bottom, though
        linewidth = 2,   
        linecolor = 'rgba(226,217,243,255)'   # Make line color same as text
    )

    fig.update_yaxes(
        showgrid=False,
        zeroline = True,   # Want one line at zero 
        zerolinewidth = 2,
        zerolinecolor = 'rgba(226,217,243,255)' # Make line color same as text
    )

    return fig

# Run app
if __name__ == '__main__':
        app.run_server(jupyter_mode='tab', debug=True)