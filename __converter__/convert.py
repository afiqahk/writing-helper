# ref: https://pypi.org/project/pypandoc/
# can also convert batch of .md files into one docx/html...
import pypandoc
import argparse
import logging
import glob
import pathlib

def parse_args():
    """Parse input arguments."""
    desc = ('Convert document from one format to another e.g. .docx to .md')
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--input', type=str, required=True,
        help="Path to input file e.g.:"
             " file in current directory, 'chapter1.docx'"
             " file in another directory, 'book1/chapter1.docx'"
             " full path, 'D:/chapter1.docx'"
             " pattern, 'book1/*.docx' (default is merge into one output, else set --multi_output)")
    parser.add_argument(
        '--format', type=str, required=True,
        help="Format to convert to (without the dot '.'), e.g.: "
             " docx | md | rtf | txt | json |"
             " html | epub | pdf (output-only)")
    parser.add_argument(
        '--output', type=str,
        help="Path to output file e.g.:"
             " file in current directory, 'chapter1.md'"
             " file in another directory, 'book1/chapter1.md'"
             " full path, 'D:/chapter1.md'")
    parser.add_argument(
        '--multi_output', type=str,
        help="Output folder if input is a pattern and you want separate output files"
             "e.g.: 'book1")
    args = parser.parse_args()
    if args.output is None and args.multi_output is None:
        raise SystemExit("Converter: must provide either 'output' or 'multi_output' option")
    return args

def convert(input, format, output):
    out = pypandoc.convert_file(input, format, outputfile=output)
    if out == "":
        print(f"Succesfully converted '{input}' to '{output}'")
    else:
        raise SystemExit(f"ERROR: can't convert requested item, {input}")
    return

def run(**kwargs):
    args = argparse.Namespace(**kwargs)
    try:
        if args.multi_output is not None:
            for file in glob.glob(args.input):
                outfile = str(pathlib.Path(args.multi_output) / (pathlib.Path(file).stem + f'.{args.format}') )
                convert(file, args.format, outfile)
        else:
            convert(args.input, args.format, args.output)        
    except Exception as e:
        # logging.exception(" " + str(e))
        logging.error(" " + str(e))
    return

def main():
    args = parse_args()
    run(**vars(args))

if __name__=="__main__":
    main()