# CrewAI Experiments

This repository contains Jupyter notebooks exploring the capabilities of CrewAI, a framework for orchestrating role-playing autonomous AI agents. These notebooks demonstrate various concepts, implementations, and practical applications of the CrewAI framework.

## Notebooks

### 1. CrewAI Concepts (crewai_concepts.md)

This notebook provides a comprehensive introduction to CrewAI, covering fundamental concepts with working code examples:

- Understanding Agent creation with roles, goals, and backstories
- Creating Tasks with clear descriptions and expected outputs
- Forming Crews to orchestrate agent collaboration
- Exploring sequential and hierarchical processes
- Implementing custom tools
- Working with memory and state management

### 2. Web Research Book Writer (websearch_book_writer.md)

This notebook shows how to leverage web search for creating factual, well-researched books:

- Using BrightData for internet research
- Researching topics in real-time with up-to-date information
- Creating structured outlines based on research findings
- Writing content that incorporates gathered information
- Saving completed books to the filesystem

## Setup and Usage

1. Install dependencies:
   ```
   pip install crewai crewai-tools
   ```

2. For web search functionality:   
   - Get the bright data credentials from [Bright Data](https://brightdata.com) and set them as environment variables:
     ```
     export BRIGHTDATA_USERNAME=your_username
     export BRIGHTDATA_PASSWORD=your_password
     ```

3. Convert notebooks to .ipynb format:
   ```
   jupytext --to notebook *.md
   ```

4. Run the notebooks in a Jupyter environment

## Implementation Details

- All notebooks use the Ollama Gemma 3 (4B parameter) model
- Books are saved to a `books` directory in Markdown format
- Code is kept simple and cohesive to ensure functionality

## Project Structure

```
CrewAI-Experiments/
├── README.md
├── notebooks/
│   ├── crewai_concepts.ipynb
│   └── websearch_book_writer.ipynb
└── books/
    └── (Generated book files)
```
