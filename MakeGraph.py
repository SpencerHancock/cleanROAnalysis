import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.express as ex
import plotly.graph_objects as go


def Bullet(X, names, Max, title):
    fig = go.Figure()
    if type(X) is list:
        if type(X[0]) is list:
            for x, name, i in zip(X, names, range(len(X))):
                fig.add_trace(
                    go.Indicator(
                        mode = "number+gauge+delta", value = x[0],
                        delta = {'reference': x[2]},
                        domain = {'x': [0.2, 1], 'y': [i/len(X), (i+1)/len(X)-(.1)]},
                        title = {'text': name},
                        gauge = {
                            'shape': "bullet",
                            'axis': {'range': [None, Max[i]]},
                            'threshold': {
                                'line': {'color': "red", 'width': 2},
                                'thickness': 0.75,
                                'value': x[2]},
                            'steps': [
                                {'range': [0, x[1]], 'color': "gray"},
                                {'range': [x[1], Max[i]], 'color': "white"}],
                            'bar': {'color': "blue"}}
                    )
                )
                fig.update_layout(
                    title={
                        'text': title,
                        'xanchor': 'center',
                        'yanchor': 'top',
                        'y':0.9,
                        'x':0.5,},
                    xaxis_title="Time",
                    font=dict(
                        family="Courier New, monospace",
                        size=18,
                        color="#7f7f7f"))
            return fig
        fig.add_trace(
            go.Indicator(
                mode = "number+gauge+delta", value = X[0],
                delta = {'reference': X[2]},
                domain = {'x': [0, 1], 'y': [.05, .25]},
                title = {'text': name},
                gauge = {
                    'shape': "bullet",
                    'axis': {'range': [None, Max]},
                    'threshold': {
                        'line': {'color': "green", 'width': 2},
                        'thickness': 0.75,
                        'value': X[2]},
                    'steps': [
                        {'range': [0, X[1]], 'color': "gray"},
                        {'range': [X[1], Max], 'color': "white"}],
                    'bar': {'color': "blue"}}
            )
        )
        fig.update_layout(
            title={
                'text': title,
                'xanchor': 'center',
                'yanchor': 'top',
                'y':0.9,
                'x':0.5,},
            xaxis_title="Time",
            font=dict(
                family="Courier New, monospace",
                size=18,
                color="#7f7f7f"))

        return fig


if __name__ == "__main__":
    fig = Bullet([[1, 2, 3],[1,2,2], [3,2,1]], ["lunch", "dinner", "desert"], 4)
    fig.show()