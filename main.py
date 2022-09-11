import pandas as pd
import plotly.express as px # 
import plotly.graph_objects as go

import dash # or use version 1.12.0
from dash import html, dcc
from dash.dependencies import Input, Output


app = dash.Dash(__name__)
# ----------------------------------------------------------------------------------------------------------

# Import and clean dataset
df = pd.read_csv('bees.csv')

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df = df.reset_index()
print(df.head())

# -----------------------------------------------------------------------------------------------------------

# App layout
app.layout = html.Div([

    html.H1('Bees fatalities Factors - Dashboard with Dash', style={'text-align': 'center'}), 

    dcc.Dropdown(id = 'select_year', 
                 options= [
                    {'label': '2015', 'value': 2015},
                    {'label': '2016', 'value': 2016},
                    {'label': '2017', 'value': 2017},
                    {'label': '2018', 'value': 2018}], 
                    multi=False, 
                    value=2015, 
                    style={'width': '40%'}
                    ), 
    html.Div(id='output_container', children=[]), 
    html.Br(), 

    dcc.Graph(id='my_bee_map', figure={})

])


# ----------------------------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'), 
     Output(component_id='my_bee_map', component_property='figure')],
     [Input(component_id='select_year', component_property='value')]
)

def update_graph(option_selected):
    print(option_selected)
    print(type(option_selected))
    
    container = 'The year chosen is {}'.format(option_selected)

    df1 = df.copy()
    df1 = df1[df1['Year'] == option_selected]
    df1 = df1[df1['Affected by'] == 'Varroa_mites']

    # Plotly Express
    fig = px.choropleth(
        data_frame=df1, 
        locationmode='USA-states', 
        locations='state_code', 
        scope='usa',
        color='Pct of Colonies Impacted', 
        hover_data=['State', 'Pct of Colonies Impacted'], 
        color_continuous_scale=px.colors.sequential.ylorrd,
        labels={'Pct of Colonies Impacted': 'Percentage of Bee Colonies'},
        template='plotly_dark'
        )


    # Plotly Grapth Objects (GO)
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states', 
            locations=df1['state_code'], 
            z = df1['Pct of Colonies Impacted'].astype(float), 
            colorscale='curl',
        )]
    )

    fig.update_layout(
        title_text='Bees Affected By Mites in the USA', 
        title_xanchor='center', 
        title_font=dict(size=24), 
        title_x=0.5, 
        geo=dict(scope='usa')
    )

    return container, fig


# ----------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)