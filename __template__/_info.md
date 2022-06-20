# Summary
*_info.md is where the folder contents should be explained*

Template files, also used to test functions. 

For each fic, put all files in a folder. Choose which files you want to merge into a folder by editing *_toc.yaml*. For proper conversion and formatting to HTML, these files must be Markdown (.md) files. Merged document will be in *_out* folder.

<br/>

# Table of Contents (TOC) structure

The TOC is defined in *_toc.yaml* file; each folder must have only one of this file. 

A fic may consist of either:
- chapter
- extra

Chapters are chapters. Extras are for any other files  (e.g. notes) that you want to merge into one document. Edit *_toc.yaml* to select which .md file will be merged. Only one chapter or one extra can be selected for merging at a time.

<br/>

## Chapter/Extra:

For convenience, chapter/extra will be referred as simply 'chapter'.

There are two components for each chapter:
- title
- parts

Title is the name of the chapter - this will be in the name of the merged document. Don't use the same title for different chapters of the same fic or previous merged chapters will be overwritten.

Parts is the individual files that will be merged into one chapter. Place them in the order you want to merge them. After merging, each part will be separated by a horizontal rule.

<br/>

## Part:

Each part consist of:
- name
- href

Name is the name of the part — this is for user reference only and not used in merging. Href is the filename.