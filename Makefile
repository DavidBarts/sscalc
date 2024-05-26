# Where things live. If defined, must end with a slash.

PANDOC_DIR =

all: README.md sccc

# Because I dislike Markdown (syntactically significant end-of-line
# whitespace, really?), I maintain the README for this project in
# reStructuredText.

%.md: %.rst
	$(PANDOC_DIR)pandoc -f rst -t markdown_strict -o $@ $<

%.html: %.rst
	$(PANDOC_DIR)pandoc -f rst -t html -o $@ $<
