from mcp.server.fastmcp import FastMCP
import random

# Create an MCP server
mcp = FastMCP("Demo Server")

# Add a simple resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}! Welcome to our MCP lab."

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

# Add a data generator tool
@mcp.tool()
def generate_data(data_type: str, count: int = 5) -> str:
    """Generate random data of the specified type
    
    Args:
        data_type: Type of data to generate ('names', 'emails', 'numbers')
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
    
    else:
        raise ValueError(f"Unknown data type: {data_type}")

# Add a documentation resource
@mcp.resource("docs://mcp")
def get_mcp_docs() -> str:
    """Get documentation about MCP"""
    return """
    # Model Context Protocol (MCP)
    
    MCP is a standardized protocol for LLMs to interact with external systems. It defines:
    
    ## Resources
    - Similar to GET endpoints in a REST API
    - Provide data to LLMs
    - Identified by URIs like 'resource://path'
    
    ## Tools
    - Similar to POST endpoints in a REST API
    - Allow LLMs to take actions
    - Have defined inputs and outputs
    
    ## Prompts
    - Reusable templates for LLM interactions
    - Can include multiple messages
    - Support customization via arguments
    """

# Add a simple prompt
@mcp.prompt()
def rag_query(query: str) -> str:
    """Create a prompt for RAG-based querying"""
    return f"""I need you to answer the following question using only the information provided from the knowledge base. 
    If the answer cannot be found in the knowledge base, please say so.
    
    Question: {query}
    """

# This is needed for direct execution
if __name__ == "__main__":
    mcp.run()
