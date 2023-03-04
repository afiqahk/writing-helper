import plotly.express as px
import pandas as pd

class ProgressTrackerPlotter:
    def __init__(self):
        return
    
    def plot_line_by_month(self, df_timeline):
        df = df_timeline
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("MS").agg(func=self.format_aggregates())
        self.format_resample_fillzero(df)
        self.format_agg_list_getunique(df)
        self.format_lists_to_html(df)
        self.plot_line(df)

    def plot_line_by_week(self, df_timeline):
        df = df_timeline
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("W").agg(func=self.format_aggregates())
        self.format_resample_fillzero(df)
        self.format_agg_list_getunique(df)
        self.format_lists_to_html(df)
        self.plot_line(df)
    
    def plot_line_by_day(self, df_timeline):
        df = df_timeline
        self.format_lists_to_html(df)
        df.index = pd.DatetimeIndex(df.index)
        df_idx_new = pd.date_range(df.index.min(), df.index.max(), freq='D')
        df = df.reindex(df_idx_new)
        self.format_missing_values(df)
        self.plot_line(df)
    
    def format_missing_values(self, df):
        df.fillna({
            "diff_wordcount": 0,
            "diff_file": "",
            "branch": "",
        }, inplace=True)
    
    def format_agg_list_getunique(self, df):        
        df.diff_file = df.diff_file.apply(lambda x: set(x))
        df.branch = df.branch.apply(lambda x: set(x))
    
    def format_lists_to_html(self, df):
        df.diff_file = df.diff_file.apply(lambda x: '<br> - '.join(x))
        df.branch = df.branch.apply(lambda x: ', '.join(x))
    
    def format_aggregates(self):
        return {
            "diff_wordcount": "sum",
            "diff_file" : "sum",
            "branch" : "sum",
        }
    def format_resample_fillzero(self, df):
        df.diff_file = df.diff_file.apply(lambda x : [] if x==0 else x)
        df.branch = df.branch.apply(lambda x : [] if x==0 else x)
    
    def rename_columns(self, df):
        df.rename(columns={
            "diff_wordcount" : "wordcount",
            "diff_file" : "file",
        }, inplace=True)
        df.index.name = "date"
    
    def plot_line(self, df):
        self.rename_columns(df)
        fig = px.line(df, x=df.index, y="wordcount", markers=True, hover_name="branch", hover_data=["file"])
        fig.show()