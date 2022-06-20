import yaml
import logging
import pathlib
import argparse

def add_toc_args(parser):
    parser.add_argument(
        '--doc', type=str, required=True,
        help="Name of document/folder e.g. '.template'")
    parser.add_argument(
        '--chapter', type=str, default=None,
        help="Name of chapter title")
    parser.add_argument(
        '--extra', type=str, default=None,
        help="Name of extra section title")
    return parser

class TableofContents:
    def __init__(self, args):
        self.args = args
        self.doc = args.doc
        self.toc = None
        self.tocpath = None
        self.counter = 0
        self._open()
        return
    
    def _open(self):
        self.tocpath = pathlib.Path() / self.doc / "_toc.yaml"
        with open(self.tocpath, 'r') as f:
            toc = yaml.load(f, Loader=yaml.SafeLoader)
        a = self.args
        if a.chapter:
            logging.info(f"TOC: using chapter {a.chapter}")
            self.toc = toc["chapters"]
            self.toc = self._find_item(a.chapter)
        elif a.extra:
            logging.info(f"TOC: using extra {a.extra}")
            self.toc = toc["extras"]
            self.toc = self._find_item(a.extra)
        else:
            raise RuntimeError('TOC: no item type specified!')
        if self.toc is not None:
            self.toc = self.toc['parts']
        return
    
    def _find_item(self, title):
        res = next((x for x in self.toc if x['title'] == title), None)
        if res is None:
            logging.warning(f"TOC: {title} not found")
        return res

    def read(self):
        res = self.toc[self.counter:self.counter+1]
        if not res:
            logging.warning("TOC: reached end")
            return None
        self.counter +=1
        return res[0]