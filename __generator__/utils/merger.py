import logging
import pathlib

class Merger:
    def __init__(self, args):
        self.doc = args.doc
        self.chapter = args.chapter
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
        OUT_FOLDER = "__out__"
        if self.chapter is not None:
            self.dest = pathlib.Path() / OUT_FOLDER / f"{self.doc}_{self.chapter}.md"
        else:
            raise RuntimeError('Merger: no item type specified!')
        
        logging.info(f" Merger: write to '{self.dest}'")
        dest_root = self.dest.parent
        dest_root.mkdir(parents=True, exist_ok=True)
        return

    def add(self, part):
        src = self.source / part['href']
        with open(src, 'r', encoding="utf8") as fin, open(self.dest.parent / (self.dest.name + ".tmp"), 'a', encoding="utf8") as fout:
            for line in fin:
                fout.write(line)
            fout.write("\n\n---\n\n") # insert horizontal rule at end of part
        logging.info(f" Merger: added part '{part['name']}' from '{src}'")
        return
    
    def clean(self):
        """Clean up the formatting. Call after finished merging
        Remove the last <hr/>
        """
        try:
            tempfile = self.dest.parent / (self.dest.name + ".tmp")
            with open(tempfile, 'r', encoding="utf8") as f:
                lines = f.readlines()
            with open(self.dest, 'w', encoding="utf8") as f:
                f.writelines(lines[:-3])
            tempfile.unlink()
        except Exception as e:
            logging.error(" Auto-clean fail, please check formatting manually. Error:")
            logging.error(e)
        return