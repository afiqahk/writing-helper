# General

Write anything using vs-code and markdown, convert it to html for easy uploading to web.

You can write snippets in separate files, organize everything via a table-of-contents and automatically merge into one document.
Also includes converter code to convert from markdown (.md) to html (.html) for easier upload to some websites.

Why use vs-code and markdown to write? Why write all this code?
- Dark mode.
- Can use Git to view file history, so I don't have to agonise over if I *really* want to delete a paragraph.
- Easier to convert between formats.
- Easier to customize the writing experience with extensions.
- Easier to see what I want to include or not in one file (_toc.yaml) without having to delete or move contents.


# Setup
Setup python environment via the environment.yml file or manually install the necessary packages:
```
    conda install -c anaconda pypandoc
    conda install -c anaconda pyyaml
```

Recommended vs-code extensions for best experience. These helps in running the python code and formatting your files and so on. Without the last one you can't use Ctrl+I for *italics*:
```
    Python - Microsoft
    YAML - Red Hat
    Markdown All in One - Yu Zhang
```

Additional vs-code extensions to make life easier. These are not strictly necessary, but is nice to have. *Noctis* is the nicest vs-code themes extension I've found fit for me, but there are many others in the Extensions Marketplace if you filter Category -> Themes.
```
    HTML Preview - George Oliveira
    Word Count - Microsoft
    HTML Related Links - rioj7
    Noctis - Liviu Schera
```
HTML Related Links is needed for easily managing file links, so you can easily ctrl+click to open and create new files all from your _toc.yaml.

Open your settings.json:
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

# How to use

1. Create a folder for your story. This folder should contain all the files for this one story.
2. Create a table-of-contents file (or copy from __template__ folder):
   ```
    _toc.yaml
   ```
   The TOC will contain all the files you want to include in your final file. The TOC consists of *chapters*. 
   Each chapter has attributes *title* and *parts* that you can set. Do not use same title for different chapters or merging will cause files to be overwriten.
   
   Each part has attribute *name* which is for your reference only, and *href* which is the link to the file with your writing. Organize parts by the order you want to merge the chapter.
   
3. To merge, edit *config.yaml* with the folder name and chapter title you want to merge. Only one chapter can be merged at a time. Each part will be separated by a horizontal rule after emrging.
    ```
    merge:
        doc: FolderName     
        chapter: ChapterTitle
    ```
    Then run the python code in the command line
    ```
        python run.py merge
    ```
    The resulting file will be in folder *```__out__```* as FolderName_ChapterTitle.md
4. To convert

# Files

*```__converter__```*

Scripts to convert markdown file to html.

*```__generator__```*

Scripts to merge separate parts of a chapter into one .md file which can be converted into HTML

*```__template__```*

Template files to serve as example and used to test scripts.
