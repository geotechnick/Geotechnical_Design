import base64
import pandas as pd
import io
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
from dash.dependencies import State


def display_row(selected_value): # function for pile info
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

def test_call(value):
    return value