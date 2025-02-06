# Define variables
CLAT_BINARY := $(shell which claat || echo $(go env GOPATH)/bin/claat)
CLAT_REPO := github.com/googlecodelabs/tools/claat
MARKDOWN_FILE := Notes.md
OUTPUT_DIR := dbt_lab

# Install claat if not already installed
install:
	@echo "Installing claat..."
	go install $(CLAT_REPO)@latest
	@echo "Claat installed successfully."

# Convert markdown to codelabs
convert: install
	@echo " Removing old codelabs..."
	rm -rf $(OUTPUT_DIR)
	@echo "Creating new codelabs..."
	@echo "Converting $(MARKDOWN_FILE) to Codelabs format..."
	$(CLAT_BINARY) export $(MARKDOWN_FILE) 
	@echo "Conversion complete!"

# Serve the codelab locally
serve:
	@echo "Serving the Codelab locally..."
	$(CLAT_BINARY) serve 

# Clean up output directory
clean:
	rm -rf $(OUTPUT_DIR)
	@echo "Cleaned up the output directory."
