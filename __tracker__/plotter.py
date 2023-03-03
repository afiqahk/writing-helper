import plotly.express as px
import pandas as pd

class ProgressTrackerPlotter:
    def __init__(self):
        return
    
    def plot_line_by_month(self, df_timeline):
        df = df_timeline
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("MS").agg({
            "diff_wordcount": "sum",
            "diff_file" : lambda x: ',\n'.join(x)
        })
        df.diff_file = df.diff_file.apply(lambda x: x.replace(',\n', '<br> - '))
        fig = px.line(df, x=df.index, y="diff_wordcount", markers=True, hover_data=["diff_file"])
        fig.show()

    def plot_line_by_week(self, df_timeline):
        df = df_timeline
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("W").agg({
            "diff_wordcount": "sum",
            "diff_file" : lambda x: ',\n'.join(x)
        })
        fig = px.line(df, x=df.index, y="diff_wordcount", markers=True, hover_data=["diff_file"])
        fig.show()
    
    def plot_line_by_day(self, df_timeline):
        df = df_timeline
        df.index = pd.DatetimeIndex(df.index)
        df_idx_new = pd.date_range(df.index.min(), df.index.max(), freq='D')
        df = df.reindex(df_idx_new)
        df.fillna({
            "diff_wordcount": 0,
            "diff_file": "",
        }, inplace=True)
        fig = px.line(df, x=df.index, y="diff_wordcount", markers=True, hover_data=["diff_file"])
        fig.show()
    
    