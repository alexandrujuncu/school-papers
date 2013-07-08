TEXDIR = texfiles
CMD = pdflatex
BASENAME = thesis
PDF = $(BASENAME).pdf

# REDIR = > /dev/null
# REDIR =

.PHONY: all clean

all:
	@rm -f $(PDF)
	$(CMD) $(BASENAME) $(REDIR)
	bibtex $(BASENAME) $(REDIR)
	$(CMD) $(BASENAME) $(REDIR)
	$(CMD) $(BASENAME) $(REDIR)

vim:
	vim -p thesis.tex chapters/01intro.tex chapters/02tech.tex chapters/03arch.tex chapters/04client.tex chapters/05server.tex chapters/06conclusions.tex
pdf:
	evince $(PDF)


clean:
	pwd
	rm chapters/*.aux
	rm thesis.{aux,bbl,blg,lof,log,lol,lot,out,pdf,toc}

