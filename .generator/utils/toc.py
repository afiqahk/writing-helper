import yaml
import logging
import pathlib
import argparse

def add_toc_args(parser):
    # ! doc
    # chapter - chapter title [chapter 'title']
    # extra - extras section [extra 'title']
    # help
    return parser

class TableofContents:
    def __init__(self, args):
        self.args = args
        self.doc = args.doc
        self.tocpath = pathlib.Path() / self.doc / "_toc.yaml"
        self.counter = 0
        self._open()
        return
    
    def _open(self):
        with open(self.tocpath, 'r') as f:
            toc = yaml.load(f, Loader=yaml.FullLoader)
        self.tocpath = self.tocpath.parent()
        a = self.args
        if a.chapter:
            logging.info(f"TOC: using chapter {a.chapter}")
            self.toc = toc["chapters"]
            self.toc = self._find_item(a.chapter)
        elif a.extra:
            logging.info(f"TOC: using extra {a.extra}")
            self.toc = toc["extras"]
            self.toc = self._find_item(a.extra)
        return
    
    def _find_item(self, title):
        res = next((x for x in self.toc if x['title'] == title), None)
        if res is None:
            raise Exception(f"TOC: {title} not found")
        return res

    def read(self):
        res = self.toc[self.counter:self.counter+1]
        if not res:
            raise Exception("TOC: reached end")
        self.counter +=1
        return res[0]