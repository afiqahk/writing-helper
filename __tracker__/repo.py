from git import Repo
import pathlib
import json
import re
import datetime
import pandas as pd
from argparse import Namespace
from __tracker__.tracker import ProgressTracker

CONFIG_FILE = "./__tracker__/tracker.config.json"

class RepoCrawler:
    def __init__(self, repo_dir=""):
        self.repo_dir = repo_dir if repo_dir else pathlib.Path.cwd()
        self.repo = Repo(self.repo_dir)
        self.change_type_to_check = [ "A", "M", "D"]

    def get_diff_between_commits(self, commit, commit_prev):
        diffs = [ d for d in commit_prev.diff(commit) if d.change_type in self.change_type_to_check]
        return diffs

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
        repo = self.repo
        args.last_checked_datetime_isoformat = "2022-12-21T15:26:04+08:00"
        branches = self.get_branches(args.exclude_branches)
        for branch in branches:
            commits = self.get_commits_since(branch.name, args.last_checked_datetime_isoformat)
            for i in range(1, len(commits)):
                newer_commit = commits[i - 1]
                older_commit = commits[i]
                diffs = self.get_diff_between_commits(newer_commit, older_commit)
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
    rc = RepoCrawler()
    rc.get_rawdata(args)
    assert True
    