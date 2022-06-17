import logging
import pathlib
import shutil

class Merger:
    def __init__(self, args):
        self.doc = args.doc
        self.chapter = args.chapter
        self.extra = args.extra
        self.source = pathlib.Path() / self.doc 
        self.dest = None
        self._setup_dest()
        return
    
    def _setup_dest(self):
        """Setup destination for single-document .md file

        Choose which item to set as destination
        Remove old destination folder and create a new one
        Create destination .md file
        """        
        if self.chapter is not None:
            self.dest = pathlib.Path() / "tmp" / f"{self.doc}_{self.chapter}.md"
        elif self.extra is not None:
            self.dest = pathlib.Path() / "tmp" / f"{self.doc}_{self.extra}.md"
        else:
            raise RuntimeError('Merger: no item type specified!')
        
        logging.info(f"Merger: write to {self.dest}")
        dest_root = self.dest.parent()
        shutil.rmtree(dest_root, ignore_errors=True)
        dest_root.mkdir(parents=True)
        return

    def add(self, part):
        src = self.source / part['href']
        with open(src, 'r') as fin, open(self.dest / ".tmp", 'a') as fout:
            for line in fin:
                fout.write(line)
            fout.write("\n---\n") # insert horizontal rule at end of part
        logging.info(f"Merger: added part {part['name']} from {src}")
        return
    
    def clean(self):
        """Clean up the formatting. Call after finished merging
        Remove the last <hr/>
        """
        try:
            with open(self.dest / ".tmp", 'r') as f:
                lines = f.readlines()
            with open(self.dest, 'w') as f:
                f.writelines(lines[:-3])
        except Exception as e:
            logging.warning("Auto-clean fail, please check formatting manually")
        return