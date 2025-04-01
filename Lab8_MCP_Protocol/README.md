# Model Context Protocol (MCP) Lab

## Overview

This repository contains materials for a 1.5-hour lab session on the Model Context Protocol (MCP) and its application in AI systems. The lab is designed for students working on big data intelligence and analytics projects.

## Lab Structure

The lab is divided into six main sections:

1. **Introduction to MCP**
   - What is MCP and why it's used
   - Core benefits and architecture

2. **MCP Protocol Fundamentals**
   - Core components: Resources, Tools, and Prompts
   - Protocol flow and message structure

3. **Working with MCP Servers**
   - Setting up the LlamaCloud MCP Server
   - Configuring Claude Desktop for MCP integration

4. **Building a Basic MCP Agent**
   - Using the Python SDK to create custom MCP servers
   - Exposing resources and tools

5. **Q&A and Next Steps**
   - Common questions and answers
   - Ideas for applying MCP in your projects

6. **OpenAI Agents MCP Integration (Bonus)**
   - Using MCP with OpenAI's Agents Python SDK
   - Comparing different MCP integration approaches

## Prerequisites

- Python 3.9+
- Claude Desktop (for MCP client integration)
- Basic understanding of LLMs and AI systems
- Access to LlamaCloud (for vector database integration)

## Setup Instructions

1. Install required Python packages:
   ```bash
   pip install "mcp[cli]" mcp-agent
   ```

2. Optional: For OpenAI Agents examples (Section 6):
   ```bash
   pip install openai-agents
   ```

3. Clone this repository:
   ```bash
   git clone <repository-url>
   cd Lab_MCP_Protocol
   ```

4. Configure your Claude Desktop with the provided MCP server settings.

5. Follow the step-by-step instructions in each markdown file.

## Code Examples

The `code` directory contains example implementations:

- `basic_mcp_server.py`: A simple MCP server with the Python SDK
- `openai_agents_mcp_example.py`: MCP integration with OpenAI Agents SDK

## Lab Delivery

For instructors, the `Lab_Delivery_Guide.md` file contains a detailed plan for delivering this lab session, including:

- Demonstration steps
- Time allocations
- Command examples
- Presentation tips

## Additional Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Python SDK Repository](https://github.com/modelcontextprotocol/python-sdk)
- [MCP Agent Framework](https://github.com/lastmile-ai/mcp-agent)
- [LlamaCloud MCP Server](https://github.com/run-llama/mcp-server-llamacloud)
- [OpenAI Agents Python SDK](https://github.com/openai/openai-agents-python)

## License

This lab material is provided for educational purposes only.
