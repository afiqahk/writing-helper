# General

Write anything using vs-code and markdown.
You can write snippets in separate files, organize everything via a table-of-contents and automatically merge into one document.
Also allow conversion to multiple formats, from various input formats e.g. markdown (.md) to HTML (.html), Microsoft Documents (.docx) to Markdown (.md) and many more (see accepted formats below).

Why use vs-code and markdown to write? Why write all this code?
- Dark mode.
- Easily switch between different writing contexts using Git branches
- Can use Git to view file history, so I don't have to agonise over if I *really* want to delete a paragraph.
- Easier to convert between formats
- Easier to customize the writing experience with extensions.
- Easier to see what I want to include or not in one file (_toc.yaml) without having to delete or move contents.


# Setup
Setup python environment via the environment.yml file:
```
    conda env create -f environment.yml
```
Or manually install the necessary packages in your python environment (I use Anaconda here):
```
    conda install -c anaconda pypandoc
    conda install -c anaconda pyyaml
```

Required vs-code extension:
```
    Python - Microsoft
```

Recommended vs-code extensions for best experience:
```
    YAML - Red Hat (check for errors in config files)
    Markdown All in One - Yu Zhang (for markdown shortcuts e.g. Ctrl+I for *italics*)
    HTML Preview - George Oliveira (for previewing or opening html files in browser (right-click))
```

Additional vs-code extensions to make life easier. These are not strictly necessary, but is nice to have. *Noctis* is the nicest vs-code themes extension I've found fit for me, but there are many others in the Extensions Marketplace if you filter Category -> Themes.
```
    Word Count - Microsoft (show word count of current file)
    HTML Related Links - rioj7  (easily create new file - see below)
    Noctis - Liviu Schera (layout theme)
```
HTML Related Links is needed for easily managing file links, so you can easily ctrl+click to open and create new files all from your _toc.yaml. For this, open your settings.json:
```
    Ctrl+Shift+P -> Preferences: Open Workspace Settings (JSON)
```
and add this:
```
    "html-related-links.include": {
        "yaml": [
            {
                "find":"href: (.*\\.md)"
            },
        ]
    },
    "html-related-links.alwaysShow": true,
    "html-related-links.enableLogging": false,
```

### **Em dash**

What's a writer without the em dash? I know for sure I'd be languishing without. If you have Windows and a full keyboard, you can simply use the Windows shortcut (Alt+0151) but this is for those of us without.

To add a shortcut for em-dash in vs-code, first add a user snippet file:
```
    Ctrl+Shift+P -> Snippets: Configure User Snippets -> New Global Snippets File
```
Then add to the .code-snippets file:
```
	"— em": {
		"prefix": "---",
		"body": "—"
	  }
```
To use, type "---" then click Ctrl+Space to get an em dash.

# How to use this repo

1. Create a folder for your story. This folder should contain all the files for this one story.
2. Create a table-of-contents file (or copy from ```__template__``` folder):
   ```
    _toc.yaml
   ```
   The TOC will contain all the files you want to include in your final file. The TOC consists of *chapters*. 
   Each chapter has attributes *title* and *parts* that you can set. Do not use same title for different chapters or merging will cause files to be overwriten.
   
   Each part has attribute *name* which is for your reference only, and *href* which is the link to the file with your writing. Organize parts by the order you want to merge the chapter.
   
3. To merge, edit *config.yaml* with the folder name and chapter title you want to merge. Only one chapter can be merged at a time. Each part will be separated by a horizontal rule after merging.
    ```
    merge:
        doc: FolderName     
        chapter: ChapterTitle
    ```
    Then run the python code in the command line
    ```
        python run.py merge
    ```
    The resulting file will be in folder ```__out__``` as FolderName_ChapterTitle.md
    
4. To convert files into a different format, edit *config.yaml*. You can convert a single file, or multiple files at a time. Example for converting a single Markdown file in subfolder to a HTML file in the same folder:
   ```
    convert:
        input: FolderName/FileName.md
        format: "html"
        output: FolderName/FileName.html
   ```
   Example for different folders:
   ```
    convert:
        input: D:/path/to/FileName.md
        format: "html"
        output: C:/path/to/somewhere/else/FileName.html
   ```
   If converting multiple files, your input files must have the same pattern, e.g. *BookA_ch1.md*, *BookA_ch2.md*, *BookA_ch3.md* with the pattern being *BookA_ch\*.md*, and then you have two options for conversion:

   Option one is convert and merge everything into one output file:
   ```
    convert:
        input: FolderName/BookA_ch*.md
        format: "html"
        output: FolderName/BookA.html
   ```
   Option two is convert into separate output files. You must provide the folder name, and the output files will have the same name as the inputs:
   ```
    convert:
        input: FolderName/BookA_ch*.md
        format: "html"
        multi_output: FolderName
   ```
   Finally after editing *config.yaml*, run the python code in command line:
   ```
    python run.py convert
   ```

   Accepted input formats:
   ```
    docx | md | rtf | txt | json | html | epub 
   ```
   Accepted output formats:
   ```
    docx | md | rtf | txt | json | html | epub | pdf
   ```
   Note that I haven't done quality checks on the converted files, so if you run into issues with conversion, please check the pypandoc repo.

## Track your progress

If you use git to keep track of your files, you can check the updated word count each day/week/month. This will generate charts of word count per time as HTML file in the current directory, 'tracker_report.html' which you can right-click to open in browser (if you have the *HTML Preview* vscode extension - see above in *Setup*)
```
    python run.py track
```

# Control Tips

- Italics: ctrl + I
- Bold: ctrl + B
- Comment/Uncomment: ctrl + /

# Files

*```__converter__```*

Scripts to convert files to different formats. Requires pypandoc.

*```__generator__```*

Scripts to merge separate parts of a chapter into one .md file which can be converted into HTML

*```__template__```*

Template files to serve as example and used to test scripts.
