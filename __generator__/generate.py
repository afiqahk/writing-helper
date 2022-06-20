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

def run(**kwargs):
    args = argparse.Namespace(**kwargs)
    toc = TableofContents(args)
    merger = Merger(args)
    if not toc.toc:
        raise SystemExit(f"ERROR: can't open toc item requested at {toc.tocpath.resolve()}")    
    loop_and_merge(toc, merger)
    return

def main():    
    args = parse_args()
    run(**vars(args))
    return

if __name__=="__main__":
    main()