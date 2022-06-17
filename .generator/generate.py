import argparse
from utils.toc import add_toc_args, TableofContents
from utils.merger import Merger

def parse_args():
    """Parse input arguments."""
    desc = ('Generate HTML document from .md parts')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_toc_args(parser)
    args = parser.parse_args()
    return args

def loop_and_merge(toc, merger):
    while True:
        part = toc.read()
        if part is None:
            break
        merger.add(part)
    merger.clean()
    return

def main():
    args = parse_args()

    toc = TableofContents(args)
    merger = Merger(args)
    if not toc.toc:
        raise SystemExit("ERROR: can't open toc item requested")    
    loop_and_merge(toc, merger)
    return

if __name__=="__main__":
    main()