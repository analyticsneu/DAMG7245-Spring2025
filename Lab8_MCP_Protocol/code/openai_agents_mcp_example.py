import asyncio
import os
import shutil
from typing import Any

# Note: You'll need to install openai-agents package
# pip install openai-agents

# Import OpenAI Agents SDK components
try:
    from agents import Agent, Runner, trace
    from agents.mcp import MCPServerStdio
except ImportError:
    print("Error: OpenAI Agents SDK not installed.")
    print("Please install it using: pip install openai-agents")
    exit(1)

async def run_filesystem_demo(samples_dir: str):
    """
    Run a demonstration of using the filesystem MCP server with OpenAI Agents.
    
    Args:
        samples_dir: Path to the directory containing sample files
    """
    print(f"Connecting to filesystem MCP server with access to: {samples_dir}")
    
    # Connect to the filesystem MCP server using stdio
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        # Create an agent with access to the MCP server
        agent = Agent(
            name="File Explorer Assistant",
            instructions=f"""You are a helpful assistant that can access files in the directory: {samples_dir}.
                          Use the MCP tools to read files and answer questions about their contents.
                          Be concise and accurate in your responses.""",
            mcp_servers=[server],
        )
        
        # Example 1: List available files
        message = "What files are available to you? List them all."
        print(f"\n\n--- Example 1: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print("\nAssistant's response:")
        print(result.final_output)
        
        # Example 2: Read a specific file
        message = "Read the contents of the favorite_books.txt file and tell me the top 3 books."
        print(f"\n\n--- Example 2: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print("\nAssistant's response:")
        print(result.final_output)
        
        # Example 3: Answer a question requiring reasoning
        message = "Look at the favorite songs file and suggest a new song I might enjoy based on my preferences."
        print(f"\n\n--- Example 3: {message}")
        result = await Runner.run(starting_agent=agent, input=message)
        print("\nAssistant's response:")
        print(result.final_output)

async def interactive_mode(samples_dir: str):
    """
    Run an interactive session with the filesystem MCP server.
    
    Args:
        samples_dir: Path to the directory containing sample files
    """
    print(f"Starting interactive mode with access to: {samples_dir}")
    print("Type 'exit', 'quit', or 'q' to exit.")
    
    # Connect to the filesystem MCP server using stdio
    async with MCPServerStdio(
        name="Filesystem Server",
        params={
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", samples_dir],
        },
    ) as server:
        # Create an agent with access to the MCP server
        agent = Agent(
            name="File Explorer Assistant",
            instructions=f"""You are a helpful assistant that can access files in the directory: {samples_dir}.
                          Use the MCP tools to read files and answer questions about their contents.
                          Be concise and accurate in your responses.""",
            mcp_servers=[server],
        )
        
        # Interactive loop
        while True:
            # Get user input
            user_input = input("\nYour query (or 'exit' to quit): ")
            
            # Check for exit command
            if user_input.lower() in ["exit", "quit", "q"]:
                print("Exiting interactive mode.")
                break
            
            # Process the query with the agent
            print("Processing...")
            result = await Runner.run(starting_agent=agent, input=user_input)
            
            # Display the result
            print("\nAssistant:")
            print(result.final_output)

async def main():
    """Main entry point for the example."""
    # Check for npx
    if not shutil.which("npx"):
        print("Error: npx is not installed.")
        print("Please install it with: npm install -g npx")
        exit(1)
    
    # Create or use sample directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    samples_dir = os.path.join(current_dir, "sample_files")
    
    # If sample_files directory doesn't exist, create it with sample content
    if not os.path.exists(samples_dir):
        os.makedirs(samples_dir)
        
        # Create sample files
        files = {
            "favorite_books.txt": """1. To Kill a Mockingbird – Harper Lee
2. Pride and Prejudice – Jane Austen
3. 1984 – George Orwell
4. The Hobbit – J.R.R. Tolkien
5. Harry Potter and the Sorcerer's Stone – J.K. Rowling
6. The Great Gatsby – F. Scott Fitzgerald
7. Charlotte's Web – E.B. White
8. Anne of Green Gables – Lucy Maud Montgomery
9. The Alchemist – Paulo Coelho
10. Little Women – Louisa May Alcott""",
            
            "favorite_songs.txt": """1. "Here Comes the Sun" – The Beatles
2. "Imagine" – John Lennon
3. "Bohemian Rhapsody" – Queen
4. "Shake It Off" – Taylor Swift
5. "Billie Jean" – Michael Jackson
6. "Uptown Funk" – Mark Ronson ft. Bruno Mars
7. "Don't Stop Believin'" – Journey
8. "Dancing Queen" – ABBA
9. "Happy" – Pharrell Williams
10. "Wonderwall" – Oasis""",
            
            "favorite_movies.txt": """1. The Shawshank Redemption (1994)
2. The Godfather (1972)
3. Pulp Fiction (1994)
4. The Dark Knight (2008)
5. Fight Club (1999)
6. Inception (2010)
7. Forrest Gump (1994)
8. The Matrix (1999)
9. Goodfellas (1990)
10. The Lord of the Rings: The Fellowship of the Ring (2001)"""
        }
        
        for filename, content in files.items():
            with open(os.path.join(samples_dir, filename), "w") as f:
                f.write(content)
        
        print(f"Created sample files in: {samples_dir}")
    else:
        print(f"Using existing sample files in: {samples_dir}")
    
    # Menu
    print("\nSelect mode:")
    print("1. Run demonstration (automated examples)")
    print("2. Interactive mode (chat with the assistant)")
    
    choice = input("Enter your choice (1 or 2): ")
    
    if choice == "1":
        # Run the demonstration
        with trace(workflow_name="MCP Filesystem Demo"):
            await run_filesystem_demo(samples_dir)
    elif choice == "2":
        # Run interactive mode
        with trace(workflow_name="MCP Interactive Mode"):
            await interactive_mode(samples_dir)
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    asyncio.run(main())
