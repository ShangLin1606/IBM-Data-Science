#!/usr/bin/env python
# coding: utf-8

# ========== IBM Data Visualization Final Assignment (Part 2) ==========
# Author: [Your Name]
# Description:
# Dash Application for Automobile Sales Statistics
# Tasks 2.1 - 2.6
# ======================================================================

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ============================================================
# Load dataset
# ============================================================
data = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/'
    'IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/'
    'historical_automobile_sales.csv'
)

# ============================================================
# Initialize Dash app
# ============================================================
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# ============================================================
# Dropdown menu options
# ============================================================
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]

year_list = [i for i in range(1980, 2024)]

# ============================================================
# Layout
# ============================================================
app.layout = html.Div([
    # ---------- 2.1 Title ----------
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#1E90FF', 'fontSize': 28}
    ),

    # ---------- 2.2 Dropdowns ----------
    html.Div([
        html.Label("Select Statistics Type:"),
        dcc.Dropdown(
            id='select-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select Statistics Type'
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=2020,
            placeholder='Select Year'
        )
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px'}),

    # ---------- 2.3 Output container ----------
    html.Div(
        id='output-container',
        className='output-container',
        style={'marginTop': 30}
    )
])

# ============================================================
# 2.4 Callbacks
# ============================================================

# Enable/disable year dropdown depending on selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='select-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True


# Callback to display charts based on selection
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    # =======================================================
    # 2.5 Recession Period Statistics
    # =======================================================
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        # Plot 1: Average Automobile Sales over Recession Period (yearly)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Fluctuation over Recession Period'
            )
        )

        # Plot 2: Average vehicles sold by vehicle type
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title='Average Vehicles Sold by Vehicle Type during Recession'
            )
        )

        # Plot 3: Pie chart - total advertisement expenditure share by vehicle type
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title='Total Advertisement Expenditure Share by Vehicle Type during Recession'
            )
        )

        # Plot 4: Effect of Unemployment Rate on Vehicle Type and Sales
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title='Effect of Unemployment Rate on Vehicle Type and Sales'
            )
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart1), html.Div(children=R_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=R_chart3), html.Div(children=R_chart4)],
                     style={'display': 'flex'})
        ]

    # =======================================================
    # 2.6 Yearly Statistics
    # =======================================================
    elif input_year and selected_statistics == 'Yearly Statistics':
        yearly_data = data[data['Year'] == input_year]

        # Plot 1: Average Automobile Sales over all years
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title='Average Automobile Sales Over Years'
            )
        )

        # Plot 2: Total Monthly Automobile Sales (All years)
        mas = data.groupby('Month')['Automobile_Sales'].mean().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title='Average Monthly Automobile Sales'
            )
        )

        # Plot 3: Average number of vehicles sold by type in selected year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f'Average Vehicles Sold by Vehicle Type in {input_year}'
            )
        )

        # Plot 4: Advertisement expenditure per vehicle type
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                names='Vehicle_Type',
                values='Advertising_Expenditure',
                title=f'Total Advertisement Expenditure by Vehicle Type in {input_year}'
            )
        )

        return [
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart1), html.Div(children=Y_chart2)],
                     style={'display': 'flex'}),
            html.Div(className='chart-item',
                     children=[html.Div(children=Y_chart3), html.Div(children=Y_chart4)],
                     style={'display': 'flex'})
        ]

    else:
        return None


# ============================================================
# Run app
# ============================================================
if __name__ == '__main__':
    app.run(debug=True)
