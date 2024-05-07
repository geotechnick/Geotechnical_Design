import pandas as pd
import io
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go

# Load CSV with all the H-Pile info
H_Pile = pd.read_csv("https://raw.githubusercontent.com/geotechnick/Geotechnical_Design/main/Pile_Design/H_Piles/HP_Spec_Table.csv")
Fy = 50  # Pile yield stress in ksi
pile_names = H_Pile['Section_E'].unique().tolist()

# Filter out the metric values
H_Pile = H_Pile.loc[:, ~H_Pile.columns.str.endswith('_M')]

# Create drop down with the pile names
dropdown = dcc.Dropdown(id='pile-dropdown', options=[{'label': name, 'value': name} for name in pile_names], value=pile_names[0])


#pile selection (note that this code only accounts for one case)##############################
def display_row(selected_value, H_Pile):
    if selected_value is None:
        return html.Div("No pile selected")
    
    pile_info = H_Pile[H_Pile['Section_E'] == selected_value]
    pile_units = H_Pile[H_Pile['Section_E'] == 'Units_English']
    pile_display = pd.concat([pile_info, pile_units], ignore_index=True)
    
    # Adds case_1 to the data frame
    old_index_label = pile_info.index[0]
    new_index_label = 'case_1'
    pile_info = pile_info.rename(index={old_index_label: new_index_label})
    pile_info.reset_index(inplace=True)

    return html.Table([html.Tr([html.Th(col), html.Td(pile_display[col].values[0])]) for col in pile_display.columns])
##################################################################################################

#importing soil csv ###########################################################
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = io.StringIO(base64.b64decode(content_string).decode('utf-8'))

    df = pd.read_csv(decoded)
    
    # Create Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=df.columns,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df[column] for column in df.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    return html.Div([
        html.H5(filename),
        html.H6("Raw Data:"),
        html.Pre(df.to_string()),
        html.H6("Interactive Table:"),
        dcc.Graph(
            id='table',
            figure=table
        ),
    ])

def update_output(contents, filename):
    if contents is not None:
        children = parse_contents(contents, filename)
        return children
################################################################################