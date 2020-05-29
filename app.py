import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as ex
import plotly.graph_objects as go

import pandas as pd

from RV import ReverseNormalize
from MakeGraph import Bullet




external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', 
                        "https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css", 
                        "https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500&display=swap",]



smallest_index = 0
# get clean plant data
df = pd.read_excel("clean_new_data.xlsx")

#get reference values for Qp, SP and DP
reference1 = []
reference2 = []
reference3 = []

for i in range(len(df.index)):
    reference1.append(df.at[1, "Q_p"])
    reference2.append(df.at[1, "SP"])
    reference3.append(df.at[1, "dp"])


fig1 = go.Figure()
# Create and style traces
fig1.add_trace(go.Scatter(x=df.Datetime, y=reference1, name='Reference', 
                        line=dict(color='grey', width=4, dash="dash")))
fig1.add_trace(go.Scatter(x=df.Datetime, y=df.NMQp, name = 'New Membrane',
                        line=dict(color='grey', width=4)))
fig1.add_trace(go.Scatter(x=df.Datetime, y=df.Q_p, name='Actual',
                        line=dict(color='royalblue', width=4) # dash options include 'dash', 'dot', and 'dashdot'
))
fig1.update_layout(title='Permeate Flow Vs. Time',
                   xaxis_title='Time',
                   yaxis_title='Permeate Flow (m3/h)')

fig2 = go.Figure()
# Create and style traces
fig2.add_trace(go.Scatter(x=df.Datetime, y=reference2, name='Reference',
                        line=dict(color='grey', width=4, dash="dash")))
fig2.add_trace(go.Scatter(x=df.Datetime, y=df.NMSP, name = 'New Membrane',
                        line=dict(color='grey', width=4)))
fig2.add_trace(go.Scatter(x=df.Datetime, y=df.SP, name='Actual',
                        line=dict(color='royalblue', width=4) # dash options include 'dash', 'dot', and 'dashdot'
))
fig2.update_layout(title='Salt Passage Vs. Time',
                   xaxis_title='Time',
                   yaxis_title='Salt Passage')

fig3 = go.Figure()
# Create and style traces
fig3.add_trace(go.Scatter(x=df.Datetime, y=reference3, name='Reference',
                        line=dict(color='grey', width=4, dash="dash")))
fig3.add_trace(go.Scatter(x=df.Datetime, y=df.NMDP, name = 'New Membrane',
                        line=dict(color='grey', width=4)))
fig3.add_trace(go.Scatter(x=df.Datetime, y=df.dp, name='Actual',
                        line=dict(color='royalblue', width=4) # dash options include 'dash', 'dot', and 'dashdot'
))
fig3.update_layout(title='Pressure Drop Vs. Time',
                   xaxis_title='Time',
                   yaxis_title='Pressure Drop')

f1 = html.H4(className="mr-0 ml-0 col-6 text-right",id = "Fouling1")
if round(df.at[len(df.index)-1, "Q_p"]-df.at[len(df.index)-1, "NMQp"], 3) < 0:
    f1 = html.H4(style={"color":"red"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling1",
                 children=round(df.at[len(df.index)-1, "Q_p"]-df.at[len(df.index)-1, "NMQp"]))
else:
    f1 = html.H4(style={"color":"black"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling1",
                 children=round(df.at[len(df.index)-1, "Q_p"]-df.at[len(df.index)-1, "NMQp"]))

html.H4(className="mr-0 ml-0 col-6 text-right",id = "Conditions1",children= round(df.at[len(df.index)-1, "NMQp"]-df.at[1, "Q_p"], 3))

c1 = 0
if round(df.at[len(df.index)-1, "NMQp"]-df.at[1, "Q_p"], 3) >= 0:
    c1 = html.H4(style={"color":"green"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions1",
                 children= round(df.at[len(df.index)-1, "NMQp"]-df.at[1, "Q_p"], 3))

else:
    c1 = html.H4(style={"color":"red"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions1",
                 children= round(df.at[len(df.index)-1, "NMQp"]-df.at[1, "Q_p"], 3))

f2 = html.H4(className="mr-0 ml-0 col-6 text-right",id = "Fouling2")
if round(df.at[len(df.index)-1, "SP"]-df.at[len(df.index)-1, "NMSP"], 3) < 0:
    f2 = html.H4(style={"color":"green"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling2",
                 children=round(df.at[len(df.index)-1, "SP"]-df.at[len(df.index)-1, "NMSP"], 3))
else:
    f2 = html.H4(style={"color":"black"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling2",
                 children=round(df.at[len(df.index)-1, "SP"]-df.at[len(df.index)-1, "NMSP"], 3))
c2 = 0
if round(df.at[len(df.index)-1, "NMSP"]-df.at[1, "SP"], 3) >= 0:
    c2 = html.H4(style={"color":"red"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions2",
                 children= round(df.at[len(df.index)-1, "NMSP"]-df.at[1, "SP"], 3))

else:
    c2 = html.H4(style={"color":"green"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions2",
                 children= round(df.at[len(df.index)-1, "NMSP"]-df.at[1, "SP"], 3))

f3 = html.H4(className="mr-0 ml-0 col-6 text-right",id = "Fouling3")
if round(df.at[len(df.index)-1, "dp"]-df.at[len(df.index)-1, "NMDP"], 3) > 0:
    f3 = html.H4(style={"color":"red"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling3",
                 children=round(df.at[len(df.index)-1, "dp"]-df.at[len(df.index)-1, "NMDP"], 3))
else:
    f3 = html.H4(style={"color":"black"}, className="mr-0 ml-0 col-6 text-right",id = "Fouling3",
                 children=round(df.at[len(df.index)-1, "dp"]-df.at[len(df.index)-1, "NMDP"], 3))
c3 = 0
if round(df.at[len(df.index)-1, "NMDP"]-df.at[1, "dp"], 3) >= 0:
    c3 = html.H4(style={"color":"red"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions3",
                 children= round(df.at[len(df.index)-1, "NMDP"]-df.at[1, "dp"], 3))

else:
    c3 = html.H4(style={"color":"green"}, className="mr-0 ml-0 col-6 text-right",id = "Conditions3",
                 children= round(df.at[len(df.index)-1, "NMDP"]-df.at[1, "dp"], 3))


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(className="bg-light",style={"margin":"0", "text-align":"center", "width":"100vw", 
                      "overflow":"hidden", "font-family": "Courier New, monospace", "color":"grey"},
                      children=[
    #==================================== Header ==================================================
    #this will include the pani logo on the far left, links, etc.
    html.Div(style={"height":"7em"},className ="navbar navbar-light bg-white", children=[
        html.A(style={"height":"60%"},className ="navbar-brand pl-4 ", href="#pani", children=[
            html.Img(style={"height":"100%"},src="data:image/png;base64,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")
        ] )
    ]),

    #=================================================selection board ========================================================================

    html.Div(className="bg-light col-2 float-left p-5", children=[
        html.Div(style={"height":"100vh"}, className="bg-white", children=[
            html.H4("Pani Energy Selection dashboard!", className="p-2")
        ]),
        #================================================= hehehehehehe ==================================================
        html.Div(className="bg-white p-5 mt-5", children=[
            html.A(href="https://www.christianmingle.com/en-us", children=[
            html.Img(style={"width":"100%"}, src="https://cminglestudy.files.wordpress.com/2013/09/christianmingle.png")
            ])
        ]),
    ]),



    #====================================   Dashboard =============================================
    # this will include the three health metrics and their changes from reference and new membrane conditions
    html.Div(style={"margin-top":"10em", "padding":"5em","box-sizing": "border-box",}, className="bg-light p-10 m-0 col-10 float-right", children=[
        html.Div(className = "row", style={"width":"100%", "margin":"0"}, children=[
            html.Div(className="col-4 pl-0 pr-5 pt-0 pb-0 m-0", id="dash1", children=[
                html.Div(className="dash row bg-white p-5 m-0 float-center", id="fix", children=[
                    html.H3("Permeate Flowrate", className="text-left"),
                    html.Div(style={"width":"100%"},id ="stats1", children=[
                        html.Div(style={"width":"100%"}, className="row float-left text-left m-0", children=[
                            html.Div(style={"width":"100%"}, className="col-12", children=[
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Reference: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Reference1",children=round(df.at[1, "Q_p"], 2)),
                                ]),
                                html.Hr(style={"width":"100%"}),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Actual: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Actual1",children=round(df.at[len(df.index)-1, "Q_p"], 2)),
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Fouling: "),
                                    f1,
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Conditions: "),
                                    c1,
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
            html.Div(className="col-4 pl-2.5 pr-2.5 pt-0 pb-0 m-0", id="dash2", children=[
                html.Div(className="dash row bg-white p-5 m-0", children=[
                    html.H3("Salt Passage", className="text-left"),
                    html.Div(style={"width":"100%"},id ="stats2", children=[
                        html.Div(style={"width":"100%"}, className="row float-left text-left m-0", children=[
                            html.Div(style={"width":"100%"}, className="col-12", children=[
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Reference: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Reference2",children=round(df.at[1, "SP"], 2)),
                                ]),
                                html.Hr(style={"width":"100%"}),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Actual: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Actual2",children=round(df.at[len(df.index)-1, "SP"], 2)),
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Fouling: "),
                                    f2,
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Conditions: "),
                                    c2,
                                ]),
                            ]),
                        ]),
                    ]),    
                ]),
            ]),
            html.Div(className="col-4 pl-5 pr-0 pt-0 pb-0 m-0", id="dash3", children=[
                html.Div(className="dash row bg-white p-5 m-0", children=[
                    html.H3("Pressure Drop", className="text-left"),
                    html.Div(style={"width":"100%"},id ="stats3", children=[
                        html.Div(style={"width":"100%"}, className="row float-left text-left m-0", children=[
                            html.Div(style={"width":"100%"}, className="col-12", children=[
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Reference: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Reference3",children=round(df.at[1, "dp"], 2)),
                                ]),
                                html.Hr(style={"width":"100%"}),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Actual: "),
                                    html.H4(className="mr-0 ml-0 col-6 text-right",id = "Actual3",children=round(df.at[len(df.index)-1, "dp"], 2)),
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Fouling: "),
                                    f3,
                                ]),
                                html.Hr(),
                                html.Div(className="row", style={"width":"100%"}, children=[
                                    html.H4(className="mr-0 ml-0 col-6 text-left",children ="Conditions: "),
                                    c3,
                                ]),
                            ]),
                        ]),
                    ]),
                ]),
            ]),
        ]),
    ]),
    
    #====================================   Graph and slider and Current values ==================================
    # this will include the graph of history with a slider to select dates

    html.Div(style={"margin-top":"0", "padding":"5em", "margin-bottom":"5em"}, className="bg-light pr-10 pl-10 pt-0 pb-0 m-0 col-10 float-right", children=[
        html.Div(className="bg-light row", children=[
            html.Div(style = {"height":"80vh", "width":"100%"}, children=[
                dcc.Graph(style={"height":"100%", "margin":"0"},id="graph-with-slider", className="col-9 m-0 float-left"),
                html.Div(style={"height":"100%", "margin":"0"},className="col-3 m-0 float-right", children=[
                    html.Div(style={"height":"100%"}, className="row bg-white p-5 m-0", children=[
                        html.H3(className="text-left d-block", id="graph-stats", children="Graph-Stats: "),
                        html.Div(style={"width":"100%"},id ="stats", children=[
                        ]),
                    ]),
                ]),
            ]),       
            html.Div(style = {"font-size":"15px", "width":"100%"},className="row pt-5", children=[

                html.B(className="col-1", children="Select Date"),

                dcc.Slider(
                    id="day-slider",
                    min=min(df.index),
                    max=len(df.Datetime),
                    value=2,
                    className="col-6"),

                html.U(id="html-date", className="col-2"),
                html.B( className="col-3")


            ]),

            html.H4(id="description",style = {"font-size":"15px"}, className="col-9 text-center float-left pt-3", children=[
                """This Mock-up is designed to communicate the performance/loss breakdown of an RO membrane. By clicking on the
                    the three panels at the top (Permeate Flow, Salt Passage, and Pressure Drop) you can toggle the graph to display
                    the history of that metric. Along the bottom of the page you can select a date and slide through the graph to 
                    get more information about any give time. The stats on the right are those at the slider value (I could have changed the titles
                    but it was a lot of work for just a mockup)."""
            ]),
        ])
    ]),

])

#========================================================= no more html ==================================================

fig = fig1

@app.callback(Output('graph-with-slider', 'figure'),
              [Input('dash1', 'n_clicks'),
               Input('dash2', 'n_clicks'),
               Input('dash3', 'n_clicks'),
               Input("day-slider", "value")])
def display(dash1, dash2, dash3, day):
    global fig
    day = day-1
    ctx = dash.callback_context

    clicked = ctx.triggered[0]["prop_id"]

    if clicked == "dash1.n_clicks":
        fig = fig1
    
    elif clicked == "dash2.n_clicks":
        fig = fig2

    elif clicked == "dash3.n_clicks":
        fig = fig3

    fig.update_layout(
        shapes=[
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= df.Datetime.at[day], x1= df.Datetime.at[day]
            )],
        font=
        dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"))

    return fig

@app.callback([Output('graph-stats', 'children'),
               Output("stats", "children"),
               Output("html-date", "children")],
              [Input("day-slider", "value")])
def SelectDate(day):
    day = day-1
    dayString = df.at[day, "Datetime"].strftime("%d-%b-%Y")
    
    df1 = df.drop(["Datetime", "Cond. At ERT to RWST [AIT - 005] [µS/cm]", "PH of ERT To RWST [AIT - 013] [-]", "FT at ERT to RWST [FT - 105] [m³/h]"], 1)

    stat_sections = []

    for column in df1.columns[1:]:
        stat_sections.append(
            html.Hr(),
        )
        stat_sections.append(
            html.Div(className="row", style={"width":"100%"}, children=[
                html.H4(className="mr-0 ml-0 col-6 text-left",children =column),
                html.H4(className="mr-0 ml-0 col-6 text-right",children=round(df1.at[day, column], 3)),
            ])
        )

    return "Graph-Stats: {}".format(dayString), stat_sections, dayString





if __name__ == '__main__':
    app.run_server(debug=True)


