# Sphinx Integration

A primary motivation for `yamldoc` was to generate documentation for YAML configuration files dynamically, in order that documentation does not outpace development. I have plans to include `yamldoc` in a Sphinx extension in the future, but for now there is a simple way to generate your parameter references with each build of the documentation. 

## Sphinx Setup

For this example, we have chosen to place our Sphinx documentation in the `docs/` folder. Inside this folder is a directory for the source scripts, a directory for the built HTML files (if building a website), and a `Makefile`.

You must first install some sort of Markdown parser so that the markdown that is produced from `yamldoc` can be understood by Sphinx. For this we recommend [`recommonmark`](https://recommonmark.readthedocs.io/en/latest/). Since there is no support for markdown style tables in this package, you have to also install [`sphinx-markdown-tables`](https://pypi.org/project/sphinx-markdown-tables/).

Install these two packages with `pip`.

```sh
pip install recommonmark sphinx-markdown-tables
```

## Sphinx Configuration

You must include these two new extensions in your sphinx documentation. Open the `source/conf.py` configuration file that Sphinx uses to load extensions, and add both of these to the list called `extensions`.

```py
extensions = [
	...
	'recommonmark',
	'sphinx_markdown_tables'
]
```

## Manual Method

If you don't mind running `yamldoc` every time you change a YAML file, you can run it manually.

Since `yamldoc` prints to STDOUT by default, just create the documentation and pipe it to a convenient file:

```sh
yamldoc your/yaml/file.yaml > docs/source/parameters.md
```

Be sure to include this in the table of contents (TOC) of your project (typically `docs/source/index.rst`)! 

## Automatic Method

If you've made it this far, you're probably in search of a "set it and forget it" method. I will be the first to admit that this is a bit hack-y, but it hasn't broken for me yet. Until I make a real Sphinx extension, edit the `docs/Makefile` in your favourite text editor. The last line should look something like this:

```make
%: Makefile
        @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

Simply add a file to generate your `parameters.md` file with `yamldoc` before any building is done with Sphinx.

```diff
%: Makefile
        yamldoc your/yaml/file.yaml > source/parameters.md`
        @$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
```

Remember to include this new file in the table of contents (TOC) for your project (typically `docs/source/index.rst`)!

For more details on how to document YAML files with `yamldoc`, see the [tutorials](tutorial.md).
