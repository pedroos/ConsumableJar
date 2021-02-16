# Consumable Jar
A repository of mathematical transcriptions and translations.

The source files are the files with a 'ctrad_' prefix in the file name (.html extension) using the following technologies:

- HTML
- CSS
- MathJax

All ready to use. A customized copy of MathJax 3 is included.

To create a new article, copy/paste one of the 'trad_' files (.html) and edit the header and footer information and replace its contents. The file will be automatically identified by the `gen2` process detailed below by its 'trad_' prefix and an output file generated.

The output files are placed in the '/out' directory.

### Compiling

- Create and configure `gen2/conf.py` from `gen2/conf.py.sample`. Personalizing `gen_dir` with your repository's absolute path is enough.
- Run the following command on the repository root (Python 3 only supported):

```
python gen2/gen.py
```

- The output files are placed in the `/out` directory.
