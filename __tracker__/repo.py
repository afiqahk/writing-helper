from git import Repo
import pathlib
import json
import re
import datetime
import pandas as pd
from argparse import Namespace
from __tracker__.tracker import ProgressTracker
from __tracker__.plotter import plot_and_save_html_report

CONFIG_FILE = "./__tracker__/tracker.config.json"

class RepoCrawler:
    def __init__(self, repo_dir=""):
        self.repo_dir = repo_dir if repo_dir else pathlib.Path.cwd()
        self.repo = Repo(self.repo_dir)
        self.change_type_to_check = [ "A", "M", "D"]

    def get_diff_between_commits(self, commit, commit_prev):
        diffs = [ d for d in commit_prev.diff(commit) if d.change_type in self.change_type_to_check]
        return diffs
    
    def filter_diffs(self, diffs):
        diffs_new = []
        for d in diffs:
            assert (d.a_path or d.b_path)
            assert(d.a_path == d.b_path)
            path = d.a_path if d.a_path else d.b_path
            regex = re.compile( r"^(\.|\_\_|\_)" )
            regex_matches = list( filter(regex.match, pathlib.Path(path).parts) )
            if (not regex_matches) and (path.endswith(".md")) and (not path.endswith("readme.md")):
                diffs_new.append(d)
        return diffs_new    

    def get_commits_since(self, branchname, since_datetime=None):
        repo = self.repo
        if since_datetime:
            if not isinstance(since_datetime, str):
                since_datetime = since_datetime.isoformat()
            return list(repo.iter_commits(branchname, since=since_datetime, no_merges=True))
        else:
            return list(repo.iter_commits(branchname, no_merges=True))

    def get_diff_wordcount(self, diff):
        if diff.a_blob is None: # new file
            a_wordcount = 0
        else:
            a_blob = diff.a_blob.data_stream.read().decode('utf-8')
            a_wordcount = len(re.findall(r'\w+', a_blob))
            
        if diff.b_blob is None: # deleted file
            b_wordcount = 0
        else:
            b_blob = diff.b_blob.data_stream.read().decode('utf-8')
            b_wordcount = len(re.findall(r'\w+', b_blob))
        return b_wordcount - a_wordcount

    def get_branches(self, excludes=[]):
        return [ b for b in self.repo.branches if b.name not in excludes ]

    def get_rawdata(self, args):
        prg = ProgressTracker()
        branches = self.get_branches(args.exclude_branches)
        for branch in branches:
            commits = self.get_commits_since(branch.name, args.last_checked_datetime_isoformat)
            for i in range(1, len(commits)):
                newer_commit = commits[i - 1]
                older_commit = commits[i]
                if (branch.name not in newer_commit.name_rev) or (branch.name not in older_commit.name_rev):
                    continue
                diffs = self.get_diff_between_commits(newer_commit, older_commit)
                diffs = self.filter_diffs(diffs)
                for diff in diffs:
                    prg.rawdata.branch.append(branch)
                    prg.rawdata.commit_datetime.append(newer_commit.committed_datetime.isoformat())
                    prg.rawdata.commit_hexsha.append(newer_commit.hexsha)
                    prg.rawdata.diff_file.append(diff.a_path)
                    prg.rawdata.diff_wordcount.append(self.get_diff_wordcount(diff))
                    prg.rawdata.diff_is_renamed.append(diff.renamed)
                    prg.rawdata.diff_is_renamed_file.append(diff.renamed_file)
                    prg.rawdata.diff_is_new_file.append(diff.new_file)
                    prg.rawdata.diff_is_deleted_file.append(diff.deleted_file)
        prg.save_raw(args.tracker_rawdata_file)
        return

def run():
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    args = Namespace(**config)
    # rc = RepoCrawler()
    # rc.get_rawdata(args)
    prg = ProgressTracker()
    # prg.read_raw(args.tracker_rawdata_file)
    # prg.save_timeline(args.tracker_data_file, data_df=prg.get_timeline())
    df = prg.read_timeline(args.tracker_data_file)
    plot_and_save_html_report(args.tracker_report_file, df)
    assert True
    
