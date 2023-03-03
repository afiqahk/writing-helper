from git import Repo
import pathlib
import json
import re
import datetime
import pandas as pd
from argparse import Namespace

CONFIG_FILE = "./__tracker__/tracker.config.json"

def get_diff_between_commits(commit, commit_prev):
    change_type_to_check = [ "A", "M", "D"]
    diffs = [ d for d in commit_prev.diff(commit) if d.change_type in change_type_to_check]
    return diffs

def get_commits_since(repo, branchname, since_datetime=None):
    if since_datetime:
        if not isinstance(since_datetime, str):
            since_datetime = since_datetime.isoformat()
        return list(repo.iter_commits(branchname, since=since_datetime, no_merges=True))
    else:
        return list(repo.iter_commits(branchname, no_merges=True))

def get_diff_wordcount(diff):
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

def get_branches(repo, excludes=[]):
    return [ b for b in repo.branches if b.name not in excludes ]

def get_rawdata(repo, args):
    data_branch = []
    data_commit_datetime = []
    data_commit_hexsha = []
    data_diff_file = []
    data_diff_wordcount = []
    data_diff_is_renamed = []
    data_diff_is_renamed_file = []
    data_diff_is_new_file = []
    data_diff_is_deleted_file = []
    
    args.last_checked_datetime_isoformat = "2022-12-21T15:26:04+08:00"
    # branch = "scara"
    branches = get_branches(repo, args.exclude_branches)
    for branch in branches:
        commits = get_commits_since(repo, branch.name, args.last_checked_datetime_isoformat)
        for i in range(1, len(commits)):
            newer_commit = commits[i - 1]
            older_commit = commits[i]
            diffs = get_diff_between_commits(newer_commit, older_commit)
            for diff in diffs:
                data_branch.append(branch)
                data_commit_datetime.append(newer_commit.committed_datetime.isoformat())
                data_commit_hexsha.append(newer_commit.hexsha)
                data_diff_file.append(diff.a_path)
                data_diff_wordcount.append(get_diff_wordcount(diff))
                data_diff_is_renamed.append(diff.renamed)
                data_diff_is_renamed_file.append(diff.renamed_file)
                data_diff_is_new_file.append(diff.new_file)
                data_diff_is_deleted_file.append(diff.deleted_file)
    df = pd.DataFrame(data={
        "data_branch": data_branch,
        "data_commit_datetime": data_commit_datetime,
        "data_commit_hexsha": data_commit_hexsha,
        "data_diff_file": data_diff_file,
        "data_diff_wordcount": data_diff_wordcount,
        "data_diff_is_renamed": data_diff_is_renamed,
        "data_diff_is_renamed_file": data_diff_is_renamed_file,
        "data_diff_is_new_file": data_diff_is_new_file,
        "data_diff_is_deleted_file": data_diff_is_deleted_file,
    })
    assert True
    return

def run():
    rw_dir = pathlib.Path.cwd()
    repo = Repo(rw_dir)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    args = Namespace(**config)
    get_rawdata(repo, args)
    assert True
    
