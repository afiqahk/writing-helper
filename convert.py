# ref: https://pypi.org/project/pypandoc/
# can also convert batch of .md files into one docx/html...
import pypandoc

def main():
    output = pypandoc.convert_file('00.rtf', 'md', outputfile="prologue.md")
    assert output == ""

if __name__=="__main__":
    main()