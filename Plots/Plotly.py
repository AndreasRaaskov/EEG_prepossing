import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np

def plot_EEG(EEG,title=""):
    """
    Plot and EEG window with plotly
    :param EEG: And EEG serie
    :param title: tutle for plot
    """


    df=EEG.to_data_frame()
    df.time = df.time / 1000
    N_chanel = len(df.columns)
    fig=go.Figure()

    for i, ch in enumerate(df.columns[1:N_chanel]):
        fig.add_trace(
            go.Scatter(x=df.time, y=df[ch], mode="lines",name=ch))
    fig.update_xaxes(title_text="time (s)")

    fig.update_layout(title=f"{title}")
    fig.show()
