from argparse import Namespace
import json
from __tracker__.progresstracker import ProgressTracker
from __tracker__.repo import RepoCrawler
from __tracker__.plotter import plot_and_save_html_report

CONFIG_FILE = "./__tracker__/tracker.config.json"

def run():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    args = Namespace(**config)
    prg = ProgressTracker()
    rc = RepoCrawler()
    rc.get_rawdata(prg.rawdata, args.exclude_branches, args.last_checked_datetime_isoformat)
    prg.save_raw(args.tracker_rawdata_file)
    prg.read_raw(args.tracker_rawdata_file)
    prg.save_timeline(args.tracker_data_file, data_df=prg.get_timeline())
    df = prg.read_timeline(args.tracker_data_file)
    plot_and_save_html_report(args.tracker_report_file, df)
    return