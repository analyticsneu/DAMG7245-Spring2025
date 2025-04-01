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