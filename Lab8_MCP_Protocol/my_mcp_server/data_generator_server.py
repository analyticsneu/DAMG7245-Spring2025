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