# Makefile for TrustEval IEEE Conference Paper

MAIN = main
BUILD_DIR = build
LATEX = pdflatex
BIBTEX = bibtex

.PHONY: all clean test

all: $(BUILD_DIR)/$(MAIN).pdf

$(BUILD_DIR)/$(MAIN).pdf: $(MAIN).tex references.bib
	mkdir -p $(BUILD_DIR)
	$(LATEX) -output-directory=$(BUILD_DIR) $(MAIN).tex
	$(BIBTEX) $(BUILD_DIR)/$(MAIN)
	$(LATEX) -output-directory=$(BUILD_DIR) $(MAIN).tex
	$(LATEX) -output-directory=$(BUILD_DIR) $(MAIN).tex

clean:
	rm -rf $(BUILD_DIR)/*

test:
	@echo "Checking LaTeX toolchain..."
	@which $(LATEX) || echo "pdflatex not found in PATH"
	@which $(BIBTEX) || echo "bibtex not found in PATH"
