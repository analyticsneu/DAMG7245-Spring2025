# Lab 3: Working with MCP Servers

## Overview

In this section, we'll focus on practical implementation of MCP servers with a particular emphasis on the LlamaCloud MCP Server. We'll explore how to configure, deploy, and interact with MCP servers to provide AI assistants with access to external data and functionality.

## Setting Up MCP Servers

MCP servers can be implemented in various languages, with official SDKs available for Python, TypeScript, and more. Each server exposes a set of resources, tools, and prompts that can be accessed by MCP clients like Claude Desktop.

### MCP Server Configuration

MCP servers are typically configured through configuration files or environment variables. For Claude Desktop, the configuration is stored in a JSON file:

- On MacOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

The configuration follows this format:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2", ...],
      "env": {
        "ENV_VAR1": "value1",
        "ENV_VAR2": "value2"
      }
    }
  }
}
```

Let's look at a complete example:

```json
{
  "mcpServers": {
    "llamacloud": {
      "command": "npx",
      "args": [
        "-y",
        "@llamaindex/mcp-server-llamacloud",
        "--index",
        "sample-docs",
        "--description",
        "Sample documentation for the lab",
        "--index",
        "course-materials",
        "--description",
        "Course materials for big data intelligence and analytics"
      ],
      "env": {
        "LLAMA_CLOUD_PROJECT_NAME": "your-project-name-here",
        "LLAMA_CLOUD_API_KEY": "your-llamacloud-api-key-here"
      }
    },
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        ""
      ],
      "env": {}
    },
    "fetch": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-fetch",
        ""
      ],
      "env": {}
    },
    "custom": {
      "command": "python",
      "args": [
        "/path/to/basic_mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

### Available MCP Servers

There are several MCP servers available for different purposes:

1. **Filesystem Server**: Provides access to local files and directories
2. **Fetch Server**: Allows fetching content from URLs
3. **LlamaCloud Server**: Connects to managed indexes on LlamaCloud
4. **SQLite Server**: Provides access to SQLite databases
5. **Custom Servers**: Created using MCP SDKs for specific use cases

## Working with LlamaCloud MCP Server

The LlamaCloud MCP Server connects to managed indexes on LlamaCloud, enabling AI assistants to perform vector search operations over your data.

### Key Features

- Creates a separate tool for each index you define
- Each tool provides a query parameter to search its specific index
- Auto-generates tool names like `get_information_index_name` based on index names
- Supports multiple indexes in a single server instance

### Setting Up LlamaCloud MCP Server

1. First, make sure you have a LlamaCloud account and have created at least one index
2. Get your LlamaCloud API key from the LlamaCloud dashboard
3. Edit your Claude Desktop configuration file to add the LlamaCloud MCP server:

```json
{
  "mcpServers": {
    "llamacloud": {
      "command": "npx",
      "args": [
        "-y",
        "@llamaindex/mcp-server-llamacloud",
        "--index",
        "your-index-name",
        "--description",
        "Description of your index",
        "--index",
        "another-index-name",
        "--description",
        "Description of another index"
      ],
      "env": {
        "LLAMA_CLOUD_PROJECT_NAME": "your-project-name",
        "LLAMA_CLOUD_API_KEY": "your-api-key"
      }
    }
  }
}
```

4. Save the configuration file and restart Claude Desktop

### Tool Definition Format

In the `args` array of the MCP config, you can define multiple tools by providing pairs of `--index` and `--description` arguments. Each pair defines a new tool.

For example:
```
--index "company-docs" --description "Internal company documentation"
```

This would add a tool for the `company-docs` LlamaCloud index to the MCP server.

## Demonstration: Claude with LlamaCloud

Let's see how Claude Desktop interacts with a LlamaCloud MCP server:

1. Configure Claude Desktop with a LlamaCloud MCP server as shown above
2. Open Claude Desktop and verify that the LlamaCloud MCP server is connected
3. Ask Claude a question that would require searching through the sample documentation, such as:
   - "What information can you find about XYZ feature in the sample documentation?"
   - "Can you summarize the key points from the sample documentation?"

Claude will:
- Use the appropriate tool to query the LlamaCloud index
- Retrieve relevant information from the index
- Incorporate the search results into its response

This demonstration shows how Claude can seamlessly access and utilize information from a vector database through the MCP protocol.

## Using Multiple MCP Servers Together

One of the strengths of MCP is the ability to use multiple servers together, combining their capabilities:

```json
{
  "mcpServers": {
    "llamacloud": {
      "command": "npx",
      "args": ["..."],
      "env": {"..."}
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", ""],
      "env": {}
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch", ""],
      "env": {}
    }
  }
}
```

This allows Claude to:
1. Search through your data using the LlamaCloud server
2. Access local files using the filesystem server
3. Fetch information from the web using the fetch server

## Testing Your Server with the MCP Inspector

To debug your LlamaCloud MCP server, you can use the MCP Inspector:

```
npm run inspector or mcp dev 
```

This will start the server and pipe its output to the MCP Inspector, allowing you to interact with it directly.

## Key Takeaways

- MCP servers provide a standardized way for AI assistants to access external data and functionality
- The LlamaCloud MCP Server enables AI assistants to search through vector indexes on LlamaCloud
- Multiple MCP servers can be used together to combine their capabilities
- The MCP Inspector is a valuable tool for debugging and testing MCP servers

## Next Steps

In the next section, we'll learn how to build a basic MCP agent using the Python SDK, which will allow us to create our own custom MCP servers.
