import pandas as pd
import datetime

class RawTrackerData:
    """ Data-only class
    """
    def __init__(self):
        self.branch = []
        self.commit_datetime = []
        self.commit_hexsha = []
        self.diff_file = []
        self.diff_wordcount = []
        self.diff_is_renamed = []
        self.diff_is_renamed_file = []
        self.diff_is_new_file = []
        self.diff_is_deleted_file = []

class ProgressTracker:
    def __init__(self):
        self.rawdata = RawTrackerData()
        self.data = pd.DataFrame()
    
    def get_rawdata_column_names(self):
        return list(vars(self.rawdata).keys())
    
    def save_raw(self, path, descendbydate=True):
        df = pd.DataFrame(data=vars(self.rawdata))        
        if descendbydate:
            df.sort_values(by=["commit_datetime"], ascending=True, inplace=True)
        df.to_csv(path, mode='a', header=not is_datafile_empty(path))
    
    def read_raw(self, path):
        df = pd.read_csv(path)
        for key, item in df.to_dict().items():
            setattr(self.rawdata, key, item)
        return df
    
    def get_unique_files(self, rawdata=None):
        if rawdata is None:
            rawdata = self.rawdata
        return list(dict.fromkeys(rawdata.diff_file))
    
    def get_timeline(self, rawdata=None):
        if rawdata is None:
            rawdata = self.rawdata
        df = pd.DataFrame(data={
            "commit_datetime": rawdata.commit_datetime,
            "diff_wordcount": rawdata.diff_wordcount,
            "diff_file": rawdata.diff_file,
        })
        df["commit_date"] = df["commit_datetime"].apply(datetime.datetime.fromisoformat).apply(lambda x: x.date().isoformat())
        return df.drop("commit_datetime", axis="columns").groupby("commit_date", as_index=True).agg({
            "diff_wordcount": "sum",
            "diff_file" : lambda x: ',\n'.join(x)
        })
    
    def save_timeline(self, path, data_df=None):
        if data_df is None:
            data_df = self.data
        data_df.to_csv(path, mode='a', header=not is_datafile_empty(path))
    
    def read_timeline(self, path):
        self.data = pd.read_csv(path)
        return self.data

    def print_timeline_pretty(self, df=None, by_month=False, by_week=False):
        if df is None:
            df = self.data
        df.index = pd.DatetimeIndex(df.index)
        if by_month:
            df = df.resample("MS").agg({
                "diff_wordcount": "sum",
                "diff_file" : lambda x: ',\n'.join(x)
                })
        elif by_week:
            df = df.resample("W").agg({
                "diff_wordcount": "sum",
                "diff_file" : lambda x: ',\n'.join(x)
                })
        else:
            df_idx_new = pd.date_range(df.index.min, df.index.max, freq='D')
            df = df.reindex(df_idx_new)

def is_datafile_empty(path):
    try:
        pd.read_csv(path, index_col=0, nrows=0)
        return True
    except pd.errors.EmptyDataError as e:
        pass
    except OSError as e:
        pass
    return False