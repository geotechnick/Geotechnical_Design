import pandas as pd
import plotly.graph_objects as go


# Load csv with all the H-Pile info
H_Pile = pd.read_csv("https://raw.githubusercontent.com/geotechnick/Geotechnical_Design/main/Pile_Design/H_Piles/HP_Spec_Table.csv")
Fy = 50  # Pile yield stress in ksi
pile_names = H_Pile['Section_E'].unique().tolist()

# Filter out the metric values
H_Pile = H_Pile.loc[:, ~H_Pile.columns.str.endswith('_M')]

# Function to display the selected row
def display_row(selected_value):
    Pile_Info = H_Pile[H_Pile['Section_E'] == selected_value]  # Creates dataframe that only has the selected value in it
    pile_units = H_Pile[H_Pile['Section_E'] == 'Units_English']  # Create separate dataframe that has units
    pile_display = pd.concat([Pile_Info, pile_units], ignore_index=True)  # Combine pile properties and pile units into single dataframe

    # Adds case_1 to the data frame
    Pile_Info = Pile_Info.rename(index={Pile_Info.index[0]: 'case_1'})  # Rename the first row to 'case_1'

    # Create a bar plot
    fig = go.Figure(data=[
        go.Bar(x=Pile_Info.columns, y=Pile_Info.iloc[0], name=selected_value)
    ])
    
    # Update layout
    fig.update_layout(
        title=f"Selected Pile Info: {selected_value}",
        xaxis_title="Properties",
        yaxis_title="Values",
        barmode='group'
    )

    fig.show()

# Create dropdown menu
dropdown = go.FigureWidget([
    go.layout.Updatemenu(
        buttons=[
            go.layout.updatemenu.Button(
                method="update",
                args=[{"visible": [True] * len(pile_names)}, {"title": "All Piles"}],
                label="All"
            )
        ],
        direction="down",
        showactive=True,
        x=0.1,
        xanchor="left",
        y=1.15,
        yanchor="top",
        bgcolor="lightgray",
        active=0,
        buttons=[{
            "label": pile_name,
            "method": "update",
            "args": [{"visible": [pile_name == pile for pile in pile_names]}, {"title": pile_name}],
        } for pile_name in pile_names]
    )
])

# Display dropdown and initial plot
display(dropdown)
display_row(pile_names[0])