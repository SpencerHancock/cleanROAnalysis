import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as ex
import plotly.graph_objects as go

import pandas as pd

from RV import ReverseNormalize
from MakeGraph import Bullet

smallest_index = 0
# get clean plant data
df = pd.read_excel("ultratech_data_clean.xlsx")
df = df.iloc[0:,0:19]
df = df.drop(["A", "B", "a", "group","resnorm"], 1)
df = df.dropna()
df = df[((df.Q_f>100))]
df = df[((df.Q_p < 100))]
df = df[((df.Q_p > 50))]
df = df[((df.index < 4000))]
df["C_f"] = df["C_f"]*0.64
df["C_p"] = df["C_p"]*0.64
df["Cond. At ERT to RWST [AIT - 005] [µS/cm]"] = df["Cond. At ERT to RWST [AIT - 005] [µS/cm]"]*.64
df["SP"] = df["C_p"]/df["C_f"]*100
df = df.reset_index()
#Q_p, Q_f, Temp, Conc_f, Conc_p, P_f, P_p, dp
#datetime,feed_flow,product_flow,reject_flow,temperature,feed_cond,reject_cond,product_cond,feed_ph,orp,reject_ph,product_ph,pressure_drop,feed_pressure,hpp_pressure,cf_pressure
RV = ReverseNormalize()
RV.set_reference(df.at[smallest_index,"Q_p"],df.at[smallest_index,"Q_f"],df.at[smallest_index,"T_f"],df.at[smallest_index,"C_f"],df.at[smallest_index,"C_p"],
                    df.at[smallest_index,"P_f"],1,df.at[smallest_index,"dp"])
df["Qpress"],df["QNM"],df["Qt"] = RV.Flow(df["Q_p"],df["Q_f"], df["T_f"],df["C_f"],df["C_p"],df["P_f"],1,df["dp"])
df["SP"], df["SPtemp"], df["SPNM"] = RV.SP(df["C_f"], df["C_p"], df["Q_f"], df["Q_p"], df["T_f"])
df["DPNM"] = RV.DP(df.Q_p, df.Q_f, df.T_f)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div(style={"margin":"auto", "text-align":"center", "width":"100vw", "overflow":"hidden"},children=[
    #==================================== Bullet Graph ============================================
    html.Div(style={"height":"100vh"}, children=[
    html.Div(style = {"height":"80%"}, className="row", children=[
        html.Div(style={"height":"90%"}, className="col-sm-1"),
        dcc.Graph(style={"height":"90%", "margin":"auto"},
                    id="graph-with-slider", className="col-10"),
        html.Div(style={"height":"90%"}, className="col-sm-1")
    ]),
    html.Div(style = {"font-size":"15px"},className="row", children=[
        html.B("Select Date: ", className="col-2"),
        dcc.Slider(
        id="day-slider2",
        min=min(df.index),
        max=len(df.Datetime),
        value=2,
        className="col-8"
            ),
        html.B(id="html-date2", className="col-2")

    ]),

    html.P(id="description",style = {"font-size":"15px", "margin":"auto"}, className="col-10"),])
    ])


@app.callback(
    [Output('graph-with-slider', 'figure'),
    Output('html-date2', 'children'),
    Output("description", "children"),
    ],
    [Input('day-slider2', 'value')])
def update_plot(selected_day):
    fig = Bullet([[df.at[selected_day, "Q_p"], df.at[selected_day, "Qpress"],df.at[selected_day, "QNM"]],
                    [df.at[selected_day, "SP"],df.at[selected_day, "SPtemp"],df.at[selected_day, "SPNM"]],
                    [df.at[selected_day, "dp"],0,df.at[selected_day, "DPNM"]]],
                    ["Product Flow", "Salt Passage", "Pressure Drop"], [100, 1.5, 1],"Normalized Performance Breakdown")
    
    return fig, df.at[selected_day, "Datetime"],"""The Bullet graph listed above represents real time changes in pressure drop, 
            salt passage and product flow rate. On the Flow Rate Graph the grey indicates 
            the current flow rate at reference pressure, the blue is current product flow rate, 
            and the red line is what the flow rate could be given a new membrane. For Salt Passage which is 
            affected differently by conditions and fouling, the blue once again represents real-time Salt Passage, 
            the grey is Salt Passage as reference temp but otherwise current conditions and the red line is salt 
            passage with a new membrane at the current conditions. For Differential Pressure or Pressure Drop, the blue is real-
            time and again the red line is pressure drop with a new membrane at the current conditions."""




if __name__ == '__main__':
    app.run_server(debug=True)