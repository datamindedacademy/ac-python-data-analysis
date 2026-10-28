.PHONY: present pdf check

# Chrome or Chromium used for PDF export; the default is the devcontainer's.
# Elsewhere: make pdf CHROME_PATH="<...>"
CHROME_PATH ?= /usr/bin/chromium

# Live preview on localhost:3030, press "p" for presenter mode
present:
	cd docs && pnpm exec slidev slides.md

# Make pdf, using CHROME_PATH, not Playwright's own Chromium download
pdf:
	cd docs && pnpm exec slidev export slides.md --output slides.pdf --executable-path "$(CHROME_PATH)"

# Check the exercise folders: exercises without outputs, and every solution runs (not the API one: make check ARGS=--with-api)
check:
	uv run python check_notebooks.py $(ARGS)
