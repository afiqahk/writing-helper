# ref: https://pypi.org/project/pypandoc/
# can also convert batch of .md files into one docx/html...
import pypandoc
import argparse
import logging

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
             " pattern, 'book1/*.docx'")
    parser.add_argument(
        '--format', type=str, required=True,
        help="Format to convert to (without the dot '.'), e.g.: "
             " docx | md | rtf | txt | json |"
             " html | epub | pdf (output-only)")
    parser.add_argument(
        '--output', type=str, required=True,
        help="Path to output file e.g.:"
             " file in current directory, 'chapter1.md'"
             " file in another directory, 'book1/chapter1.md'"
             " full path, 'D:/chapter1.md'")
    args = parser.parse_args()
    return args

def run(**kwargs):
    args = argparse.Namespace(**kwargs)
    try:
        output = pypandoc.convert_file(args.input, args.format, outputfile=args.output)
        if output == "":
            print(f"Succesfully converted '{args.input}' to '{args.output}'")
        else:
            raise SystemExit(f"ERROR: can't convert requested item, {args.input}")
    except Exception as e:
        logging.error(" " + str(e))
    return

def main():
    args = parse_args()
    run(**vars(args))

if __name__=="__main__":
    main()