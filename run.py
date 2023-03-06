import yaml
import argparse

from __generator__ import generate
from __converter__ import convert
from __tracker__ import track

def parse_args():
    """Parse input arguments."""
    desc = ('Convert document from one format to another e.g. .docx to .md')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        'command', type=str,
        help="Command to run [ convert | merge | track ]")
    parser.add_argument(
        '--clean', action="store_true",
        help=("If command==tracker, reset tracker."
        " This will delete tracker data files and"
        " the next run of tracker will get commits from the start of the repo")
    )
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    with open("config.yaml", 'r') as f:
        config = yaml.load(f, Loader=yaml.SafeLoader)
    if args.command == 'merge':
        generate.run(**config['merge'])
    elif args.command == 'convert':
        convert.run(**config['convert'])
    elif args.command == 'track':
        if args.clean:
            track.clean()
        else:
            track.run()
            print()
            print(f"Note: To reset all tracker data, run 'python run.py track --clean'")
    else:
        raise SystemExit(f"ERROR: Invalid command {args.command}")

if __name__=="__main__":
    main()