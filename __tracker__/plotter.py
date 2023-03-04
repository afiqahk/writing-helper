import plotly.express as px
import pandas as pd

class ProgressTrackerPlotter:
    def __init__(self):
        return
    
    def plot_line_by_month(self, df_timeline, show=False):
        df = df_timeline.copy()
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("MS").agg(func=self.format_aggregates())
        self.format_resample_fillzero(df)
        self.format_agg_list_getunique(df)
        self.format_lists_to_html(df)
        fig = self.plot_line(df)
        if show:
            fig.show()
        return fig

    def plot_line_by_week(self, df_timeline, show=False):
        df = df_timeline.copy()
        df.index = pd.DatetimeIndex(df.index)
        df = df.resample("W").agg(func=self.format_aggregates())
        self.format_resample_fillzero(df)
        self.format_agg_list_getunique(df)
        self.format_lists_to_html(df)
        fig = self.plot_line(df)
        if show:
            fig.show()
        return fig
    
    def plot_line_by_day(self, df_timeline, show=False):
        df = df_timeline.copy()
        self.format_lists_to_html(df)
        df.index = pd.DatetimeIndex(df.index)
        df_idx_new = pd.date_range(df.index.min(), df.index.max(), freq='D')
        df = df.reindex(df_idx_new)
        self.format_missing_values(df)
        fig = self.plot_line(df)
        if show:
            fig.show()
        return fig
    
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
        return fig

def figures_to_html(figs, filename="dashboard.html"):
    with open(filename, 'w') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:
            inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")

def plot_and_save_html_report(html_path, df_timeline):
    if df_timeline.empty:
        raise ValueError("Empty tracker data dataframe!")
    figs = []
    fig_titles = [ f"Word count per {t}" for t in ["day", "week", "month"] ]
    ptp = ProgressTrackerPlotter()
    figs.append(ptp.plot_line_by_day(df_timeline))
    figs.append( ptp.plot_line_by_week(df_timeline))
    figs.append( ptp.plot_line_by_month(df_timeline))
    for f,t in zip(figs, fig_titles):
        f.update_layout(title=t)
    figures_to_html(figs, html_path)