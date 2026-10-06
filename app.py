import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# ---------------------------------------------------------
# Load Dataset
# ---------------------------------------------------------
DATA_URL = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/d51iMGfp_t0QpO30Lym-dw/automobile-sales.csv'
data = pd.read_csv(DATA_URL)

# ---------------------------------------------------------
# Initialize Dash Application
# ---------------------------------------------------------
app = dash.Dash(__name__)
app.title = "Automobile Statistics Dashboard"

year_list = [i for i in range(1980, 2024, 1)]

# ---------------------------------------------------------
# Dashboard Layout
# ---------------------------------------------------------
app.layout = html.Div([
    html.H1(
        "Automobile Sales Statistics Dashboard",
        style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 26, 'marginTop': '15px'}
    ),
    
    # Dropdown Menus Division
    html.Div([
        html.Div([
            html.Label("Select Statistics:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='dropdown-statistics',
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                placeholder='Select a report type',
                value='Select Statistics',
                style={'width': '90%', 'padding': '3px', 'fontSize': '18px'}
            )
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Select Year:", style={'fontWeight': 'bold', 'fontSize': '16px'}),
            dcc.Dropdown(
                id='select-year',
                options=[{'label': i, 'value': i} for i in year_list],
                placeholder='Select Year',
                style={'width': '90%', 'padding': '3px', 'fontSize': '18px'}
            )
        ], style={'width': '50%', 'display': 'inline-block'})
    ], style={'padding': '15px', 'backgroundColor': '#F8F9FA', 'borderRadius': '8px', 'margin': '10px 0'}),
    
    # Output Display Division
    html.Div([
        html.Div(id='output-container', className='chart-grid', style={'display': 'flex', 'flexDirection': 'column'})
    ])
], style={'padding': '20px', 'fontFamily': 'sans-serif'})


# ---------------------------------------------------------
# Callbacks
# ---------------------------------------------------------
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    """Enable year selection only when Yearly Statistics is selected."""
    if selected_statistics == 'Yearly Statistics':
        return False
    return True


@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    """Dynamically render report charts based on user selections."""
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]
        
        # Plot 1: Automobile sales fluctuation over Recession Period (line chart)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales Fluctuation Over Recession Period"
            )
        )
        
        # Plot 2: Average number of vehicles sold by vehicle type (bar chart)
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Number of Vehicles Sold by Vehicle Type During Recession"
            )
        )
        
        # Plot 3: Total expenditure share by vehicle type during recessions (pie chart)
        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Total Advertising Expenditure Share by Vehicle Type During Recession"
            )
        )
        
        # Plot 4: Effect of unemployment rate on vehicle type and sales (bar chart)
        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='unemployment_rate',
                y='Automobile_Sales',
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title="Effect of Unemployment Rate on Vehicle Type and Sales During Recession"
            )
        )
        
        return [
            html.Div(className='chart-row', children=[html.Div(children=R_chart1, style={'width': '50%'}), html.Div(children=R_chart2, style={'width': '50%'})], style={'display': 'flex'}),
            html.Div(className='chart-row', children=[html.Div(children=R_chart3, style={'width': '50%'}), html.Div(children=R_chart4, style={'width': '50%'})], style={'display': 'flex'})
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == input_year]
        
        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales For The Whole Period"
            )
        )
        
        # Plot 2: Total Monthly Automobile sales using line chart
        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                mas,
                x='Month',
                y='Automobile_Sales',
                title=f"Total Monthly Automobile Sales in the Year {input_year}"
            )
        )
        
        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f"Average Vehicles Sold by Vehicle Type in the Year {input_year}"
            )
        )
        
        # Plot 4: Total Advertisement Expenditure for each vehicle using pie chart
        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f"Total Advertisement Expenditure for Each Vehicle in the Year {input_year}"
            )
        )
        
        return [
            html.Div(className='chart-row', children=[html.Div(children=Y_chart1, style={'width': '50%'}), html.Div(children=Y_chart2, style={'width': '50%'})], style={'display': 'flex'}),
            html.Div(className='chart-row', children=[html.Div(children=Y_chart3, style={'width': '50%'}), html.Div(children=Y_chart4, style={'width': '50%'})], style={'display': 'flex'})
        ]
        
    return None


# ---------------------------------------------------------
# Run Server
# ---------------------------------------------------------
if __name__ == '__main__':
    if hasattr(app, 'run'):
        app.run(debug=True)
    else:
        app.run_server(debug=True)
