import pandas as pd

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

class TrackerData:
    def __init__(self):
        self.commit_date = [] #columns
        self.file = [] #rows
        self.wordcount = [] #data

class ProgressTracker:
    def __init__(self):
        self.rawdata = RawTrackerData()
    
    def get_rawdata_column_names(self):
        return list(vars(self.rawdata).keys())
    
    def save_raw(self, path):
        df = pd.DataFrame(data=vars(self.rawdata))
        df.to_csv(path, mode='a', header=not is_datafile_empty(path))

def is_datafile_empty(path):
    try:
        pd.read_csv(path, index_col=0, nrows=0)
        return True
    except pd.errors.EmptyDataError as e:
        pass
    except OSError as e:
        pass
    return False
        
    

    

    