TEXDIR = texfiles
CMD = pdflatex
BASENAME = thesis
PDF = $(BASENAME).pdf

# REDIR = > /dev/null
# REDIR =

.PHONY: all

all:
	@rm -f $(PDF)
	$(CMD) $(BASENAME) $(REDIR)
	bibtex $(BASENAME) $(REDIR)
	$(CMD) $(BASENAME) $(REDIR)
	$(CMD) $(BASENAME) $(REDIR)

	evince $(PDF)
vim:
	vim -p thesis.tex chapters/01intro.tex chapters/02tech.tex chapters/03arch.tex chapters/04client.tex chapters/05server.tex chapters/06conclusions.tex
pdf:
	evince thesis.pdf
