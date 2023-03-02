from git import Repo
import pathlib
import json
import datetime

CONFIG_FILE = "./__tracker__/tracker.config.json"

def get_diff_between_commits(commit, commit_prev):
    change_type_to_check = [ "A", "M", "D"]
    diffs = [ d for d in commit.diff(commit_prev) if d.change_type in change_type_to_check]
    return diffs

def get_commits_since(repo, branchname, since_datetime):
    if not isinstance(since_datetime, str):
        since_datetime = since_datetime.isoformat()
    return list(repo.iter_commits(branchname, since=since_datetime, no_merges=True))

def run():
    rw_dir = pathlib.Path.cwd()
    repo = Repo(rw_dir)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    dtm_str = "2023-02-24T17:29:43+08:00"
    dtm_str2 = "2022-06-16T21:34:58+08:00"
    commits = get_commits_since(repo, "scara", dtm_str)
    for i in range(len(commits) - 1):
        diffs = get_diff_between_commits(commits[i+1], commits[i])
        assert True
    assert True
    
