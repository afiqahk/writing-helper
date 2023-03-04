from argparse import Namespace
import json
import datetime
import contextlib
import pathlib
import traceback
from __tracker__.progresstracker import ProgressTracker
from __tracker__.repo import RepoCrawler
from __tracker__.plotter import plot_and_save_html_report

class TrackerManager:
    def __init__(self) -> None:
        self.config_file = "./__tracker__/tracker.config.json"
        self.config = {}
    
    def config_load(self):
        with open(self.config_file, "r") as f:
            config = json.load(f)
        self.config = config
        return Namespace(**config)
    
    def config_update(self):
        completed_datetime = datetime.datetime.now().astimezone()
        self.config["last_checked_datetime_isoformat"] = completed_datetime.isoformat(timespec="seconds")
        self.config["last_checked_date"] = completed_datetime.date().isoformat()        
        with open(self.config_file, "w") as f:
            json.dump(self.config, f, indent=4)
    
    @contextlib.contextmanager
    def open(self):
        args = self.config_load()
        try:
            yield args
            self.config_update()
        except Exception as e:
            print(traceback.format_exc())
            print(f"Error: {e}")
            pathlib.Path(self.config["tracker_data_file"]).unlink(missing_ok=True)
            pathlib.Path(self.config["tracker_rawdata_file"]).unlink(missing_ok=True)


def run():
    tm = TrackerManager()
    with tm.open() as args:
        prg = ProgressTracker()
        rc = RepoCrawler()
        print("Getting raw data from git repo...")
        rc.get_rawdata(prg.rawdata, args.exclude_branches, args.last_checked_datetime_isoformat)
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