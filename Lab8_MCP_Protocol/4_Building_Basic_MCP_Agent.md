# Lab 4: Building a Basic MCP Agent with Python SDK

## Overview

In this section, we'll dive into creating our own MCP server using the Python SDK. We'll learn how to build a custom MCP server that exposes resources, tools, and prompts to AI assistants, allowing them to interact with our data and functionality.

## Introduction to the Python SDK

The Python SDK for MCP provides a high-level interface for creating MCP servers and clients. It handles the protocol details, allowing you to focus on implementing your business logic.

Key features of the Python SDK:
- Create MCP servers that expose resources, prompts and tools
- Use standard transports like stdio and SSE
- Handle MCP protocol messages and lifecycle events
- Deploy your server for use with MCP clients like Claude Desktop

## Setting Up Your Development Environment

1. Install the MCP Python SDK:
   ```bash
   pip install mcp
   ```

2. Create a new directory for your MCP server project:
   ```bash
   mkdir my_mcp_server
   cd my_mcp_server
   ```

## Creating a Basic MCP Server

Let's examine a simple MCP server that provides some basic functionality:

```python
# server.py
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("My First Server")

# Add a simple resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to our MCP server."

# Add a simple tool
@mcp.tool()
def calculate(operation: str, a: float, b: float) -> float:
    """Perform a mathematical operation
    
    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number
    
    Returns:
        Result of the operation
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    else:
        raise ValueError(f"Unknown operation: {operation}")

# Add a simple prompt
@mcp.prompt()
def math_help(problem: str) -> str:
    """Create a prompt for mathematical help"""
    return f"""I need help solving this mathematical problem:

{problem}

Please break down the solution step by step."""

# This is needed for direct execution
if __name__ == "__main__":
    mcp.run()
```

## Understanding the Code

1. **Server Creation**: `mcp = FastMCP("My First Server")` creates a new MCP server with a name.

2. **Resource Definition**:
   ```python
   @mcp.resource("greeting://{name}")
   def get_greeting(name: str) -> str:
       """Get a personalized greeting"""
       return f"Hello, {name}! Welcome to our MCP server."
   ```
   This creates a resource that returns a greeting message for the given name.

3. **Tool Definition**:
   ```python
   @mcp.tool()
   def calculate(operation: str, a: float, b: float) -> float:
       """Perform a mathematical operation..."""
       # Function implementation
   ```
   This creates a tool that performs a mathematical operation based on the provided parameters.

4. **Prompt Definition**:
   ```python
   @mcp.prompt()
   def math_help(problem: str) -> str:
       """Create a prompt for mathematical help"""
       return f"""I need help solving this mathematical problem: ..."""
   ```
   This creates a prompt template for mathematical help.

5. **Execution**: `mcp.run()` starts the server, making it available for clients to connect.

## Advanced MCP Server Features

Let's explore some more advanced features:

### Working with Images

```python
from mcp.server.fastmcp import FastMCP, Image
from PIL import Image as PILImage
import io

mcp = FastMCP("Advanced Server")

@mcp.tool()
def create_ascii_art(text: str, width: int = 40) -> str:
    """Convert text to ASCII art"""
    import pyfiglet
    return pyfiglet.figlet_format(text, width=width)

@mcp.tool()
def create_placeholder_image(width: int, height: int, color: str = "blue") -> Image:
    """Create a simple colored placeholder image"""
    img = PILImage.new('RGB', (width, height), color=color)
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return Image(data=buffer.getvalue(), format="png")
```

### Accessing Context

```python
from mcp.server.fastmcp import FastMCP, Context
import asyncio

mcp = FastMCP("Context Server")

@mcp.tool()
async def process_files(files: list[str], ctx: Context) -> str:
    """Process multiple files with progress tracking"""
    results = []
    for i, file in enumerate(files):
        ctx.info(f"Processing {file}")
        await ctx.report_progress(i, len(files))
        
        try:
            # Simulate file processing
            await asyncio.sleep(1)  # In a real server, you'd process the file here
            results.append(f"Processed {file}")
        except Exception as e:
            ctx.error(f"Error processing {file}: {str(e)}")
    
    return "\n".join(results)
```

## Data Generator MCP Server Example

Let's examine a more practical example that generates different types of data on demand:

```python
# data_generator_server.py
from mcp.server.fastmcp import FastMCP
import random
import json
from datetime import datetime, timedelta

# Create an MCP server
mcp = FastMCP("Data Generator")

# Add a tool to generate random data
@mcp.tool()
def generate_data(data_type: str, count: int = 5) -> str:
    """Generate random data of the specified type
    
    Args:
        data_type: Type of data to generate ('names', 'emails', 'numbers', 'dates')
        count: Number of items to generate
    
    Returns:
        Generated data as a string
    """
    if data_type == "names":
        first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
        return "\n".join([f"{random.choice(first_names)} {random.choice(last_names)}" for _ in range(count)])
    
    elif data_type == "emails":
        domains = ["example.com", "test.org", "demo.net", "sample.io"]
        names = ["alice", "bob", "charlie", "david", "emma", "frank"]
        return "\n".join([f"{random.choice(names)}{random.randint(1, 999)}@{random.choice(domains)}" for _ in range(count)])
    
    elif data_type == "numbers":
        return "\n".join([str(random.randint(1, 1000)) for _ in range(count)])
    
    elif data_type == "dates":
        today = datetime.now()
        return "\n".join([(today + timedelta(days=random.randint(-365, 365))).strftime("%Y-%m-%d") for _ in range(count)])
    
    else:
        raise ValueError(f"Unknown data type: {data_type}")

# Add a tool to generate structured data
@mcp.tool()
def generate_structured_data(data_type: str, count: int = 5) -> str:
    """Generate random structured data of the specified type
    
    Args:
        data_type: Type of data to generate ('users', 'products', 'transactions')
        count: Number of items to generate
    
    Returns:
        Generated data as a JSON string
    """
    if data_type == "users":
        first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson"]
        domains = ["example.com", "test.org", "demo.net", "sample.io"]
        
        users = []
        for i in range(count):
            first_name = random.choice(first_names)
            last_name = random.choice(last_names)
            email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
            age = random.randint(18, 65)
            
            users.append({
                "id": i + 1,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "age": age
            })
        
        return json.dumps(users, indent=2)
    
    elif data_type == "products":
        categories = ["Electronics", "Clothing", "Home", "Books", "Toys"]
        adjectives = ["Amazing", "Incredible", "Premium", "Budget", "Deluxe"]
        nouns = ["Gadget", "Widget", "Tool", "Device", "Pack"]
        
        products = []
        for i in range(count):
            name = f"{random.choice(adjectives)} {random.choice(nouns)}"
            price = round(random.uniform(9.99, 199.99), 2)
            stock = random.randint(0, 100)
            
            products.append({
                "id": i + 1,
                "name": name,
                "category": random.choice(categories),
                "price": price,
                "stock": stock
            })
        
        return json.dumps(products, indent=2)
    
    elif data_type == "transactions":
        statuses = ["Completed", "Pending", "Failed", "Refunded"]
        payment_methods = ["Credit Card", "PayPal", "Bank Transfer", "Crypto"]
        
        transactions = []
        for i in range(count):
            amount = round(random.uniform(10.00, 500.00), 2)
            date = (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d")
            
            transactions.append({
                "id": i + 1,
                "date": date,
                "amount": amount,
                "status": random.choice(statuses),
                "payment_method": random.choice(payment_methods),
                "user_id": random.randint(1, 100)
            })
        
        return json.dumps(transactions, indent=2)
    
    else:
        raise ValueError(f"Unknown data type: {data_type}")

# Add a resource for documentation
@mcp.resource("docs://data-generator")
def get_docs() -> str:
    """Documentation for the data generator tool"""
    return """
    # Data Generator Tool
    
    This tool generates random data of various types:
    
    ## Simple Data Types
    - **names**: Random first and last name combinations
    - **emails**: Random email addresses
    - **numbers**: Random integers between 1 and 1000
    - **dates**: Random dates within a year of the current date
    
    ## Structured Data Types
    - **users**: Random user records with ID, name, email, and age
    - **products**: Random product records with ID, name, category, price, and stock
    - **transactions**: Random transaction records with ID, date, amount, status, payment method, and user ID
    
    You can specify the number of items to generate using the 'count' parameter.
    """

# This is needed for direct execution
if __name__ == "__main__":
    mcp.run()
```

## Running and Testing Your MCP Server

### Development Mode

The fastest way to test and debug your server is with the MCP Inspector:

```bash
mcp dev data_generator_server.py
```

This will start your server and launch the MCP Inspector, allowing you to interact with it directly.

In the MCP Inspector, you can:
1. View the available tools and resources
2. Call the `generate_data` and `generate_structured_data` tools with different parameters
3. Read from the `docs://data-generator` resource
4. Observe the requests and responses

### Installing in Claude Desktop

Once your server is ready, you can install it in Claude Desktop:

```bash
mcp install data_generator_server.py --name "Data Generator"
```

To give it a custom name:

```bash
mcp install data_generator_server.py --name "Random Data Provider"
```

To provide environment variables:

```bash
mcp install data_generator_server.py -v API_KEY=abc123 -v DB_URL=postgres://...
```

## Using Your MCP Server with Claude

After installing your server in Claude Desktop, you can ask Claude to use the tools and resources provided by your server:

1. Open Claude Desktop
2. Ask Claude to generate some data, such as:
   - "Can you generate 10 random names for me?"
   - "I need a list of 5 random product records in JSON format."
   - "What data types does the data generator tool support?"

Claude will:
- Recognize the need to use your MCP server
- Call the appropriate tool with the right parameters
- Return the generated data in its response

This demonstrates how you can extend Claude's capabilities with your own custom functionality through MCP.

## Key Takeaways

- The Python SDK provides a high-level interface for creating MCP servers
- You can easily expose resources, tools, and prompts to AI assistants
- The MCP Inspector is a valuable tool for testing and debugging your servers
- The `mcp` command-line tool simplifies development and deployment
- Custom MCP servers can significantly extend the capabilities of AI assistants

## Next Steps

In the next section, we'll learn how to integrate MCP with multi-agent RAG systems, combining the power of MCP with retrieval-augmented generation techniques.
