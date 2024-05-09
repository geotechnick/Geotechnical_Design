import pandas as pd
import io
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


#pile selection (note that this code only accounts for one case)##############################
def display_row(selected_value, H_Pile):
    if selected_value is None:
        return html.Div("No pile selected")
    
    Pile_Info = H_Pile[H_Pile['Section_E'] == selected_value]
    pile_units = H_Pile[H_Pile['Section_E'] == 'Units_English']
    pile_display = pd.concat([Pile_Info, pile_units], ignore_index=True)
    
    # Adds case_1 to the data frame
    old_index_label = Pile_Info.index[0]
    new_index_label = 'case_1'
    Pile_Info = Pile_Info.rename(index={old_index_label: new_index_label})
    Pile_Info.reset_index(inplace=True)

    return html.Table([html.Tr([html.Th(col), html.Td(pile_display[col].values[0])]) for col in pile_display.columns])
##################################################################################################

#importing soil csv ###########################################################
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = io.StringIO(base64.b64decode(content_string).decode('utf-8'))

    Layer_Properties = pd.read_csv(decoded)
    
    # Create Plotly table
    table = go.Figure(data=[go.Table(
        header=dict(values=Layer_Properties.columns,
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[Layer_Properties[column] for column in Layer_Properties.columns],
                   fill_color='lavender',
                   align='left'))
    ])
    
    return html.Div([
        html.H5(filename),
        html.H6("Raw Data:"),
        html.Pre(Layer_Properties.to_string()),
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

#Analysis Options#########################################################################
def create_dataframe(n_clicks, ground_surface, top_pile, pile_length, predrill_depth, steel_strength):
    if n_clicks > 0:
        data = {
            "Ground Surface": [ground_surface],
            "Top Pile": [top_pile],
            "Pile Length": [pile_length],
            "Predrill Depth": [predrill_depth],
            "Steel Strength": [steel_strength]
        }
        Pile_Axial_Info = pd.DataFrame(data)
        
        ## adds case_1 to the data frame
        # Get the current index label of the first row
        old_index_label = Pile_Axial_Info.index[0]

        # Define the new label for the first row
        new_index_label = 'case_1'

        # Rename the first row
        Pile_Axial_Info = Pile_Axial_Info.rename(index={old_index_label: new_index_label})

        # Now the first row is renamed and shifted
        Pile_Axial_Info.reset_index(inplace=True)

        return html.Pre(Pile_Axial_Info.to_string())
    
    #Save dataframes into JSON######################################################
    