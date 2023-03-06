from argparse import Namespace
import json
import datetime
import contextlib
import pathlib
import shutil
import traceback
from __tracker__.progresstracker import ProgressTracker
from __tracker__.repo import RepoCrawler
from __tracker__.plotter import plot_and_save_html_report

class TrackerManager:
    def __init__(self) -> None:
        self.config_file = "./__tracker__/tracker.config.json"
        self.datafile_fields = {
            "tracker_rawdata_file" : "__tracker__/tracker_rawdata.csv",
            "tracker_data_file": "__tracker__/tracker_data.csv",
            "tracker_report_file": "tracker_report.html",
        }
        self.default_config = {
            "last_checked_date": "",
            "last_checked_datetime_isoformat": "",
            "tracker_rawdata_file": "__tracker__/tracker_rawdata.csv",
            "tracker_data_file": "__tracker__/tracker_data.csv",
            "tracker_report_file": "tracker_report.html",
            "exclude_branches": [
                "main",
                "initial",
                "feature_trackupdate",
                "fix_non_unicode"
            ],
            "exclude_files": "NOT IMPLEMENTED. Files starting with or inside folders starting with '.' (period), '_' (underscore) or '__' (double underscore) will be automatically filtered out"
        }
        self.config = {}
    
    def config_load(self):
        print(f"Loading tracker config file '{self.config_file}'...")
        with open(self.config_file, "r") as f:
            config = json.load(f)
        self.config = config
        self.config_check()
        print("...Finished loading tracker config file")
        return Namespace(**config)
    
    def config_check(self):
        field = "last_checked_datetime_isoformat"
        if self.config[field]:
            try:
                datetime.datetime.fromisoformat(self.config[field])
            except ValueError:
                message = (
                    f"...Field '{field}' must be in correct ISO format e.g.\n"
                    f"    '2023-03-05' (YYYY-MM-DD),\n"
                    f"    '2023-03-05T06:21:30+08:00' (YYYY-MM-DD separator HH:MM:SS Timezone),\n"
                    f"    '2023-03-05 06:21:30' (YYYY-MM-DD HH:MM:SS - will default to UTC timezone),\n"
                    )
                raise Exception(message)
            
        for field, default in self.datafile_fields.items():
            if not self.config[field]:
                print(f"...Field '{field}' cannot be empty. Using default value '{default}'")
                self.config[field] = default
        
        field = "exclude_branches"
        if not isinstance(self.config[field], list):
            message = (f"...Field '{field}' must be a list e.g. ['main', 'initial']")
            raise Exception(message)
    
    def config_update(self, new_config={}):
        if new_config:
            self.config = new_config
        else:
            completed_datetime = datetime.datetime.now().astimezone()
            self.config["last_checked_datetime_isoformat"] = completed_datetime.isoformat(timespec="seconds")
            self.config["last_checked_date"] = completed_datetime.date().isoformat()
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)
    
    def backup_data_files(self):
        data_files = [ self.config[x] for x in self.datafile_fields.keys() ]
        for f in data_files:
            p = pathlib.Path(f)
            if p.exists():
                shutil.copy(p, pathlib.Path(f"{f}.bkup"))
        
    def restore_data_files(self):
        data_files = [ self.config[x] for x in self.datafile_fields.keys() ]
        for f in data_files:
            pathlib.Path(f).unlink(missing_ok=True)
            p_bkup = pathlib.Path(f"{f}.bkup")
            if p_bkup.exists():
                p_bkup.rename(f)
    
    def delete_backup_files(self):
        data_files = [ self.config[x] for x in self.datafile_fields.keys() ]
        for f in data_files:
            pathlib.Path(f"{f}.bkup").unlink(missing_ok=True)
    
    @contextlib.contextmanager
    def open(self):
        try:
            args = self.config_load()
        except Exception as e:
            print(e)
            exit()
        self.backup_data_files()
        try:
            yield args
            self.config_update()
        except Exception as e:
            print(traceback.format_exc())
            print(f"Error: {e}")
            self.restore_data_files()
        self.delete_backup_files()

def clean():
    tm = TrackerManager()
    tm.config_load()
    print("Cleaning up tracker files...")
    for filetype in tm.datafile_fields.keys():
        pathlib.Path(tm.config[filetype]).unlink(missing_ok=True)
        print(f"...Deleted {filetype} at '{tm.config[filetype]}'")
    tm.config_update(tm.default_config)
    print("...Resetted config file to defaults")

def run():
    tm = TrackerManager()
    with tm.open() as args:
        prg = ProgressTracker()
        rc = RepoCrawler()
        print("Getting raw data from git repo...")
        rc.get_rawdata(prg.rawdata, args.exclude_branches, args.last_checked_datetime_isoformat)
        if prg.rawdata.empty():
            print(f"...No new commits found")
        else:
            prg.save_raw(args.tracker_rawdata_file)
            print(f"...Saved to '{args.tracker_rawdata_file}'")
        
        print("Getting tracker data from raw data...")
        prg.read_raw(args.tracker_rawdata_file)
        prg.save_timeline(args.tracker_data_file, data_df=prg.get_timeline())
        print(f"...Saved to '{args.tracker_data_file}'")
        
        print(f"Drawing tracker data report...")
        df = prg.read_timeline(args.tracker_data_file)
        plot_and_save_html_report(args.tracker_report_file, df)
        print(f"...Finished. Open '{args.tracker_report_file}' in browser (right-click on file)")
    return