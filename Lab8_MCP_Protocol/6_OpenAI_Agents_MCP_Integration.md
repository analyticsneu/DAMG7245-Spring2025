# Lab 6: OpenAI Agents MCP Integration

## Overview

In this bonus section, we'll explore how to integrate MCP with OpenAI's Agents Python SDK. This provides another approach to working with MCP servers, complementing what we've learned so far about the Python SDK.

## Introduction to OpenAI Agents Python SDK

The OpenAI Agents Python SDK is a framework for building AI agents using OpenAI's models. It provides an elegant way to integrate MCP servers, allowing your agents to leverage external tools and data through the Model Context Protocol.

Key features of the OpenAI Agents SDK for MCP integration:

- Native support for both Standard I/O (stdio) and Server-Sent Events (SSE) MCP transports
- Simplified agent creation with MCP server lists
- Tool caching for improved performance
- Tracing capabilities for debugging and monitoring

## MCP Server Connection Types

OpenAI's implementation supports two main types of MCP server connections:

### 1. MCPServerStdio

This class connects to MCP servers that communicate via standard input/output (stdio). Most MCP servers use this transport mechanism, including the filesystem server, git server, and others.

```python
from agents.mcp import MCPServerStdio

# Connect to a filesystem MCP server
async with MCPServerStdio(
    name="Filesystem Server",
    params={
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"],
    },
) as server:
    # Use the server
    pass
```

### 2. MCPServerSse

This class connects to MCP servers that use Server-Sent Events (SSE) for communication. This is less common but can be useful for web-based servers or integrations with cloud services.

```python
from agents.mcp import MCPServerSse

# Connect to an SSE MCP server
async with MCPServerSse(
    name="SSE Server",
    params={
        "url": "http://localhost:8000/sse",
    },
) as server:
    # Use the server
    pass
```

## Example: Filesystem MCP Server

Let's examine how to use the Filesystem MCP server with OpenAI Agents:

```python
import asyncio
import os
import shutil
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio

async def run(mcp_server):
    # Create an agent with access to the MCP server
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to read the filesystem and answer questions based on those files.",
        mcp_servers=[mcp_server],
    )
    
    # Ask the agent to list files
    message = "Read the files and list them."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    
    # Ask about specific file content
    message = "What is my #1 favorite book?"
    print(f"\n\nRunning: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    # Get the path to sample files
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")
    
    # Connect to the filesystem MCP server
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        # Run the example with the server
        with trace(workflow_name="MCP Filesystem Example"):
            await run(server)

if __name__ == "__main__":
    # Check for npx
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    
    # Run the example
    asyncio.run(main())
```

This example:
1. Creates an MCP server connection to the filesystem server
2. Creates an agent with access to that server
3. Asks the agent to list files and read specific content
4. Uses the OpenAI tracing system to log and debug the interaction

## Example: Git MCP Server

Similarly, we can connect to the Git MCP server to analyze Git repositories:

```python
import asyncio
import shutil
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio

async def run(mcp_server, directory_path):
    # Create an agent with access to the MCP server
    agent = Agent(
        name="Assistant",
        instructions=f"Answer questions about the git repository at {directory_path}, use that for repo_path",
        mcp_servers=[mcp_server],
    )
    
    # Ask about contributors
    message = "Who's the most frequent contributor?"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    
    # Ask about recent changes
    message = "Summarize the last change in the repository."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    # Ask the user for the directory path
    directory_path = input("Please enter the path to the git repository: ")
    
    # Connect to the git MCP server
    async with MCPServerStdio(
        cache_tools_list=True,  # Cache the tools list for better performance
        params={"command": "uvx", "args": ["mcp-server-git"]},
    ) as server:
        # Run the example with the server
        with trace(workflow_name="MCP Git Example"):
            await run(server, directory_path)

if __name__ == "__main__":
    # Check for uvx
    if not shutil.which("uvx"):
        raise RuntimeError("uvx is not installed. Please install it with `pip install uvx`.")
    
    # Run the example
    asyncio.run(main())
```

## Creating Custom MCP Servers with OpenAI Agents

You can also create your own MCP servers to use with OpenAI Agents. Here's an example of a simple SSE server:

```python
import random
import requests
from mcp.server.fastmcp import FastMCP

# Create server
mcp = FastMCP("Echo Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    print(f"[debug-server] add({a}, {b})")
    return a + b

@mcp.tool()
def get_secret_word() -> str:
    """Get a random secret word"""
    print("[debug-server] get_secret_word()")
    return random.choice(["apple", "banana", "cherry"])

@mcp.tool()
def get_current_weather(city: str) -> str:
    """Get the current weather for a city"""
    print(f"[debug-server] get_current_weather({city})")
    endpoint = "https://wttr.in"
    response = requests.get(f"{endpoint}/{city}")
    return response.text

if __name__ == "__main__":
    mcp.run(transport="sse")
```

To use this server with OpenAI Agents:

```python
import asyncio
import subprocess
import time
import os
from agents import Agent, Runner, trace
from agents.mcp import MCPServerSse

async def run(mcp_server):
    # Create an agent with access to the MCP server
    agent = Agent(
        name="Assistant",
        instructions="Use the tools to answer the questions.",
        mcp_servers=[mcp_server],
    )
    
    # Use the add tool
    message = "Add these numbers: 7 and 22."
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)
    
    # Use the weather tool
    message = "What's the weather in Tokyo?"
    print(f"Running: {message}")
    result = await Runner.run(starting_agent=agent, input=message)
    print(result.final_output)

async def main():
    # Connect to the SSE MCP server
    async with MCPServerSse(
        name="SSE Python Server",
        params={
            "url": "http://localhost:8000/sse",
        },
    ) as server:
        # Run the example with the server
        with trace(workflow_name="SSE Example"):
            await run(server)

if __name__ == "__main__":
    # Start the SSE server in a subprocess
    this_dir = os.path.dirname(os.path.abspath(__file__))
    server_file = os.path.join(this_dir, "server.py")
    
    process = None
    try:
        # Run the server
        print("Starting SSE server at http://localhost:8000/sse ...")
        process = subprocess.Popen(["python", server_file])
        
        # Give it time to start
        time.sleep(3)
        print("SSE server started. Running example...\n")
        
        # Run the example
        asyncio.run(main())
    finally:
        # Stop the server
        if process:
            process.terminate()
```

## Integration in Your Projects

To integrate OpenAI Agents with MCP in your own projects:

1. Install the necessary packages:
   ```bash
   pip install openai-agents
   ```

2. Identify or create MCP servers for your use case.

3. Configure your agents to use those servers:
   ```python
   from agents import Agent, Runner
   from agents.mcp import MCPServerStdio
   
   # Define your MCP servers
   filesystem_server = MCPServerStdio(
       params={"command": "npx", "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]},
   )
   
   # Create an agent with multiple MCP servers
   agent = Agent(
       name="Multi-Tool Assistant",
       instructions="You have access to files and other tools. Use them to help the user.",
       mcp_servers=[filesystem_server, other_server],
   )
   
   # Run your agent
   result = await Runner.run(starting_agent=agent, input=user_input)
   ```

## Key Differences from Traditional Function Calling

While both OpenAI Agents SDK with MCP and traditional function calling allow models to interact with tools, there are some key differences:

1. **Standardization**:
   - MCP: Provides a standardized protocol that works across different LLM providers
   - Function Calling: Often specific to a particular LLM provider's API

2. **Architecture**:
   - MCP: Uses a client-server model with clear separation of concerns
   - Function Calling: Typically relies on direct function registration within the application

3. **Tool Discovery**:
   - MCP: Supports dynamic discovery of available tools
   - Function Calling: Tools are typically statically registered

4. **Richer Primitives**:
   - MCP: Includes resources and prompts in addition to tools
   - Function Calling: Primarily focused on function/tool execution

## Practical Exercise: Creating a Simple OpenAI Agent with MCP

To demonstrate how to create a simple OpenAI Agent with MCP, let's implement a basic file explorer:

```python
# file_explorer.py
import asyncio
import os
import shutil
from agents import Agent, Runner, trace
from agents.mcp import MCPServerStdio

async def run_file_explorer(directory_path):
    # Create an MCP server for the filesystem
    async with MCPServerStdio(
        name="Filesystem Explorer",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", directory_path],
        },
    ) as server:
        # Create an agent with access to the MCP server
        agent = Agent(
            name="File Explorer",
            instructions=f"""You are a helpful file explorer assistant. 
                          You have access to the directory at {directory_path}.
                          Help the user navigate, search, and interact with files in this directory.""",
            mcp_servers=[server],
        )
        
        # Interactive mode
        print(f"File Explorer Assistant initialized with access to: {directory_path}")
        print("Type 'exit' to quit.")
        
        while True:
            # Get user input
            user_input = input("\nYour query: ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting File Explorer Assistant.")
                break
            
            # Process the query with the agent
            print("Processing...")
            result = await Runner.run(starting_agent=agent, input=user_input)
            
            # Display the result
            print("\nAssistant:")
            print(result.final_output)

if __name__ == "__main__":
    # Check for npx
    if not shutil.which("npx"):
        raise RuntimeError("npx is not installed. Please install it with `npm install -g npx`.")
    
    # Get directory path
    default_path = os.path.expanduser("~")
    path_input = input(f"Enter directory path to explore (default: {default_path}): ")
    directory_path = path_input if path_input else default_path
    
    # Validate path
    if not os.path.isdir(directory_path):
        print(f"Error: {directory_path} is not a valid directory.")
        exit(1)
    
    # Run the file explorer
    asyncio.run(run_file_explorer(directory_path))
```

This example:
1. Creates an MCP server for the filesystem
2. Creates an agent with access to that server
3. Runs an interactive loop where users can ask questions about files
4. The agent uses the MCP tools to navigate and interact with the filesystem

## Conclusion

The OpenAI Agents Python SDK provides a powerful and elegant way to integrate MCP servers into your AI applications. By combining the simplicity of OpenAI Agents with the flexibility of MCP, you can build sophisticated applications that leverage external tools and data sources.

In this section, we've explored:
- How to connect to MCP servers using both stdio and SSE
- How to create agents that use MCP tools
- How to implement custom MCP servers
- How to build interactive applications using MCP and OpenAI Agents

This approach complements what we've learned about the Python SDK, giving you another option for building MCP-enabled AI applications.

## Resources

- [OpenAI Agents Python SDK GitHub Repository](https://github.com/openai/openai-agents-python)
- [MCP Examples in OpenAI Agents](https://github.com/openai/openai-agents-python/tree/main/examples/mcp)
- [OpenAI Platform Documentation](https://platform.openai.com/docs)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
