# Lab 2: MCP Protocol Fundamentals

## Overview

In this section, we'll dive deeper into the core components of the Model Context Protocol (MCP) and understand how the protocol works at a fundamental level. We'll explore the key building blocks of MCP and how they interact within a standardized framework.

## Core Components of MCP

The Model Context Protocol defines three primary components that form the foundation of any MCP-based integration:

### 1. Resources

Resources are how you expose data to LLMs. They're similar to GET endpoints in a REST API - they provide data but shouldn't perform significant computation or have side effects.

**Key characteristics:**
- Read-only access to data
- Can be static or dynamic
- Identified by URIs with patterns like `resource://path` or `resource://{param}/path`
- Application-controlled: The client application decides when to load resources

**Examples:**
```python
@mcp.resource("config://app")
def get_config() -> str:
    """Static configuration data"""
    return "App configuration here"

@mcp.resource("users://{user_id}/profile")
def get_user_profile(user_id: str) -> str:
    """Dynamic user data"""
    return f"Profile data for user {user_id}"
```

### 2. Tools

Tools let LLMs take actions through your server. Unlike resources, tools are expected to perform computation and have side effects.

**Key characteristics:**
- Can modify data or perform operations
- Have clearly defined inputs and outputs
- Model-controlled: The LLM decides when to use tools
- Support asynchronous operation

**Examples:**
```python
@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m ** 2)

@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weather.com/{city}")
        return response.text
```

### 3. Prompts

Prompts are reusable templates that help LLMs interact with your server effectively. They provide structured guidance for specific interactions.

**Key characteristics:**
- Define interaction patterns
- Can include multiple messages
- User-controlled: The user explicitly invokes prompts
- Support customization via arguments

**Examples:**
```python
@mcp.prompt()
def review_code(code: str) -> str:
    return f"Please review this code:\n\n{code}"

@mcp.prompt()
def debug_error(error: str) -> list[Message]:
    return [
        UserMessage("I'm seeing this error:"),
        UserMessage(error),
        AssistantMessage("I'll help debug that. What have you tried so far?")
    ]
```

## Protocol Flow

MCP follows a predictable flow of communication between clients and servers:

1. **Initialization**: The client and server establish a connection and exchange capability information
2. **Discovery**: The client queries available resources, tools, and prompts
3. **Interaction**: The client reads resources, calls tools, or uses prompts as needed
4. **Termination**: The client closes the connection when done

![MCP Protocol Flow](https://modelcontextprotocol.io/images/mcp-protocol-flow.svg)

## MCP Message Structure

MCP messages follow a standardized JSON format for communication:

### Request Format
```json
{
  "id": "message-id",
  "type": "request-type",
  "params": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

### Response Format
```json
{
  "id": "message-id",
  "type": "response-type",
  "result": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

### Error Format
```json
{
  "id": "message-id",
  "type": "error",
  "error": {
    "code": "error-code",
    "message": "Error description",
    "data": { "additional": "error data" }
  }
}
```

## Server Capabilities

MCP servers declare capabilities during initialization:

| Capability | Feature Flag | Description |
|------------|--------------|-------------|
| prompts | listChanged | Prompt template management |
| resources | subscribe, listChanged | Resource exposure and updates |
| tools | listChanged | Tool discovery and execution |
| logging | - | Server logging configuration |
| completion | - | Argument completion suggestions |

## Demonstration: MCP Inspector

The MCP Inspector is a tool that allows you to interact with MCP servers directly and inspect the messages being exchanged. This helps you understand the protocol better and debug server implementations.

Let's examine a basic MCP server with the Inspector:

```python
# echo_server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Echo")

@mcp.resource("echo://{message}")
def echo_resource(message: str) -> str:
    """Echo a message as a resource"""
    return f"Resource echo: {message}"

@mcp.tool()
def echo_tool(message: str) -> str:
    """Echo a message as a tool"""
    return f"Tool echo: {message}"

@mcp.prompt()
def echo_prompt(message: str) -> str:
    """Create an echo prompt"""
    return f"Please process this message: {message}"
```

To run this server with the MCP Inspector:

```bash
mcp dev echo_server.py
```

In the Inspector UI, we can:
1. View the capabilities of the echo server
2. List available resources, tools, and prompts
3. Call the echo_tool with a test message
4. Read from the echo resource with different parameters

This demonstration shows the inner workings of MCP communication and helps visualize how clients and servers interact.

## Key Takeaways

- MCP provides a structured way for LLMs to interact with external systems through three primary mechanisms: Resources, Tools, and Prompts
- The protocol defines a standardized message format for clients and servers to communicate
- The flow of interaction is predictable and follows a clear lifecycle
- MCP Inspector is a valuable tool for understanding and debugging MCP server implementations

## Next Steps

In the next section, we'll learn how to work with MCP servers in practice, focusing on setting up and configuring LlamaCloud MCP Server for integration with Claude Desktop.
