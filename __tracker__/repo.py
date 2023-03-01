from git import Repo
import pathlib
import json

CONFIG_FILE = "./__tracker__/tracker.config.json"

def get_diff_between_commit(commit, commit_prev, config):
    diffs = [ d for d in commit.diff(commit_prev) ]
    print()


def run():
    rw_dir = pathlib.Path.cwd()
    repo = Repo(rw_dir)
    with open(CONFIG_FILE) as f:
        config = json.load(f)
    head = repo.heads["scara"]
    hcommit = head.commit
    # iterate through parents
    print()
    # get_diff_between_commit(head.commit,)
    
    
