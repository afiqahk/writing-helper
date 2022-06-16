import logging
import pathlib
import argparse

def add_toc_args(parser):
    # ! fic
    # chapter ['title']
    # extra ['section']
    # help
    return parser

class TableofContents:
    def __init__(self, args):
        self.args = args
        self.fic = args.fic
        self._open()
        return
    
    def _open(self):
        a = self.args
        if a.chapter:
            logging.info(f"TOC: using chapter {a.chapter}")
        elif a.extra:
            logging.info("TOC: using extra {a.extra}")
        return
    
    def read(self):
        return
    
    def _read_chapter(self):
        return
    
    def _read_extra(self):
        return
