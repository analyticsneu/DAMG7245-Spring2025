"""
Chunk Visualizer - A tool to visualize different chunking strategies
"""

import os
import json
import shutil
import tiktoken
import matplotlib.pyplot as plt
import numpy as np

def save_chunks_to_json(chunks, strategy_name, output_dir="output"):
    """
    Save chunks to a JSON file for later analysis or reference.
    
    Args:
        chunks: List of text chunks
        strategy_name: Name of the chunking strategy
        output_dir: Directory to save the JSON file
        
    Returns:
        Path to the JSON file
    """
    # Create strategy directory if it doesn't exist
    strategy_dir = os.path.join(output_dir, strategy_name)
    os.makedirs(strategy_dir, exist_ok=True)
    
    # Create a JSON object with chunk information
    chunks_data = {
        "strategy": strategy_name,
        "chunk_count": len(chunks),
        "chunks": []
    }
    
    # Add each chunk with metadata
    for i, chunk in enumerate(chunks):
        encoder = tiktoken.get_encoding("cl100k_base")
        chunk_info = {
            "id": i,
            "text": chunk,
            "char_length": len(chunk),
            "token_length": len(encoder.encode(chunk))
        }
        chunks_data["chunks"].append(chunk_info)
    
    # Save to JSON file
    output_path = os.path.join(strategy_dir, "chunks.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(chunks_data, f, indent=2)
    
    print(f"Chunks saved to {output_path}")
    return output_path


def visualize_chunks_html(document, chunks, output_path="chunk_visualization.html", title="Chunk Visualization", strategy_name=None):
    """
    Create an HTML visualization of chunks in a document.
    
    Args:
        document: Original text document
        chunks: List of text chunks
        output_path: Path to save the HTML file
        title: Title for the visualization
        strategy_name: Name of the chunking strategy for output directory organization
        
    Returns:
        Path to the generated HTML file
    """
    # Handle output directory based on strategy name
    if strategy_name:
        # Create strategy directory if it doesn't exist
        strategy_dir = os.path.join("output", strategy_name)
        os.makedirs(strategy_dir, exist_ok=True)
        
        # Update output path to be in the strategy directory
        filename = os.path.basename(output_path)
        output_path = os.path.join(strategy_dir, filename)
    
    # Create a list of (start_idx, end_idx, chunk_id) tuples
    chunk_positions = []
    for i, chunk in enumerate(chunks):
        # Find all occurrences of this chunk in the document
        # (Some chunking strategies might create duplicate chunks)
        start_pos = 0
        while True:
            start_idx = document.find(chunk, start_pos)
            if start_idx == -1:
                break
            chunk_positions.append((start_idx, start_idx + len(chunk), i))
            start_pos = start_idx + 1
    
    # If no chunks were found (possible with some semantic chunkers that modify text),
    # use a fuzzy matching approach
    if not chunk_positions:
        print("Warning: Could not locate exact chunks in document. Using approximate matching.")
        for i, chunk in enumerate(chunks):
            # Find a chunk by its first 30 characters
            if len(chunk) > 30:
                start_text = chunk[:30]
                start_idx = document.find(start_text)
                if start_idx != -1:
                    chunk_positions.append((start_idx, start_idx + len(chunk), i))
    
    # Sort by start position
    chunk_positions.sort()
    
    # Create HTML with different colors for chunks
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                line-height: 1.6; 
                margin: 0;
                padding: 20px;
                max-width: 1200px;
                margin: 0 auto;
                background-color: #f9f9f9;
            }}
            h1, h2 {{ color: #333; }}
            .controls {{
                position: sticky;
                top: 0;
                background-color: #f9f9f9;
                padding: 10px 0;
                margin-bottom: 20px;
                border-bottom: 1px solid #ddd;
                z-index: 100;
            }}
            .chunk {{ 
                display: inline; 
                padding: 2px 0; 
                border-radius: 3px;
                transition: opacity 0.3s;
            }}
            .overlap {{ 
                background-color: #FFD700 !important; 
                background-image: repeating-linear-gradient(45deg, transparent, transparent 5px, rgba(255,255,255,0.5) 5px, rgba(255,255,255,0.5) 10px);
            }}
            .metrics {{
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                margin-bottom: 20px;
            }}
            .metric-card {{
                background-color: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                flex: 1;
                min-width: 200px;
            }}
            .metric-title {{
                font-weight: bold;
                margin-bottom: 5px;
                color: #555;
            }}
            .metric-value {{
                font-size: 24px;
                font-weight: bold;
            }}
            button {{
                background-color: #4CAF50;
                border: none;
                color: white;
                padding: 8px 16px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 14px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 4px;
            }}
            #highlight-toggle {{
                background-color: #f44336;
            }}
            .legend {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin-bottom: 20px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                margin-right: 15px;
            }}
            .legend-color {{
                width: 20px;
                height: 20px;
                margin-right: 5px;
                border-radius: 3px;
            }}
    """.format(title=title)
    
    # Add styles for different chunks (10 different colors that repeat for more chunks)
    colors = [
        "#FFCCCC", "#CCFFCC", "#CCCCFF", "#FFFFCC", "#FFCCFF", 
        "#CCFFFF", "#FFDDBB", "#DDBBFF", "#BBFFDD", "#DDFFBB"
    ]
    
    for i in range(min(len(chunks), 50)):  # Limit to 50 chunks for performance
        html += f".chunk{i % 10} {{ background-color: {colors[i % 10]}; }}\n"
    
    html += """
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        
        <div class="controls">
            <button id="highlight-toggle" onclick="toggleHighlights()">Hide Highlights</button>
            <button onclick="showAllChunks()">Show All Chunks</button>
            <button onclick="hideAllChunks()">Hide All Chunks</button>
            
            <div class="chunk-buttons">
                <span>Toggle chunk: </span>
    """.format(title=title)
    
    # Add buttons for each chunk
    for i in range(min(len(chunks), 20)):  # Limit to first 20 chunks for UI
        html += f'<button onclick="toggleChunk({i})">{i+1}</button>\n'
    
    html += """
            </div>
        </div>
        
        <div class="metrics">
            <div class="metric-card">
                <div class="metric-title">Total Chunks</div>
                <div class="metric-value">{total_chunks}</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Avg Chunk Size</div>
                <div class="metric-value">{avg_chunk_size} chars</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Min/Max Size</div>
                <div class="metric-value">{min_chunk_size}/{max_chunk_size}</div>
            </div>
            <div class="metric-card">
                <div class="metric-title">Overlap Regions</div>
                <div class="metric-value">{overlap_count}</div>
            </div>
        </div>
        
        <div class="legend">
            <h3>Legend:</h3>
    """.format(
        total_chunks=len(chunks),
        avg_chunk_size=int(sum(len(c) for c in chunks) / len(chunks)) if chunks else 0,
        min_chunk_size=min(len(c) for c in chunks) if chunks else 0,
        max_chunk_size=max(len(c) for c in chunks) if chunks else 0,
        overlap_count=sum(1 for i in range(len(chunk_positions) - 1) 
                         for j in range(i+1, len(chunk_positions)) 
                         if chunk_positions[i][1] > chunk_positions[j][0])
    )
    
    # Add legend items for chunks
    for i in range(min(len(chunks), 10)):  # Show first 10 chunks in legend
        html += f"""
            <div class="legend-item">
                <div class="legend-color chunk{i % 10}"></div>
                <div>Chunk {i+1}</div>
            </div>
        """
    
    # Add legend item for overlaps
    html += """
            <div class="legend-item">
                <div class="legend-color overlap"></div>
                <div>Overlap</div>
            </div>
        </div>
        
        <h2>Document with Chunks Highlighted:</h2>
        <pre id="text">
    """
    
    # Build the HTML content with spans for each chunk
    text_segments = []
    
    # Sort positions by start position
    chunk_positions.sort(key=lambda x: x[0])
    
    # Create a list of all boundaries (start or end of chunks)
    boundaries = []
    for start, end, chunk_id in chunk_positions:
        boundaries.append((start, "start", chunk_id))
        boundaries.append((end, "end", chunk_id))
    
    # Sort boundaries
    boundaries.sort()
    
    # Process boundaries to generate HTML
    active_chunks = set()
    last_pos = 0
    
    for pos, boundary_type, chunk_id in boundaries:
        # Add text before this boundary
        if pos > last_pos:
            text = document[last_pos:pos]
            # If no active chunks, it's plain text
            if not active_chunks:
                text_segments.append(text)
            else:
                # Check if this is an overlap region
                is_overlap = len(active_chunks) > 1
                classes = " ".join([f"chunk{cid % 10}" for cid in active_chunks])
                if is_overlap:
                    classes += " overlap"
                
                text_segments.append(f'<span class="chunk {classes}" data-chunks="{",".join(map(str, active_chunks))}">{text}</span>')
            
            last_pos = pos
        
        # Update active chunks
        if boundary_type == "start":
            active_chunks.add(chunk_id)
        else:  # boundary_type == "end"
            if chunk_id in active_chunks:
                active_chunks.remove(chunk_id)
    
    # Add any remaining text
    if last_pos < len(document):
        text_segments.append(document[last_pos:])
    
    html += "".join(text_segments)
    
    html += """
        </pre>
        
        <script>
            let highlightsVisible = true;
            
            function toggleHighlights() {
                highlightsVisible = !highlightsVisible;
                document.querySelectorAll('.chunk').forEach(chunk => {
                    chunk.style.backgroundColor = highlightsVisible ? '' : 'transparent';
                });
                document.getElementById('highlight-toggle').textContent = 
                    highlightsVisible ? 'Hide Highlights' : 'Show Highlights';
            }
            
            function showAllChunks() {
                document.querySelectorAll('.chunk').forEach(chunk => {
                    chunk.style.opacity = '1';
                });
            }
            
            function hideAllChunks() {
                document.querySelectorAll('.chunk').forEach(chunk => {
                    chunk.style.opacity = '0.1';
                });
            }
            
            function toggleChunk(id) {
                document.querySelectorAll(`.chunk${id % 10}`).forEach(chunk => {
                    const chunks = chunk.getAttribute('data-chunks').split(',').map(Number);
                    if (chunks.includes(id)) {
                        chunk.style.opacity = chunk.style.opacity === '1' ? '0.1' : '1';
                    }
                });
            }
        </script>
    </body>
    </html>
    """
    
    # Write the HTML file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Chunk visualization saved to {output_path}")
    return output_path

def analyze_chunks_stats(chunks, use_tokens=False):
    """
    Generate comprehensive statistics for a list of chunks.
    
    Args:
        chunks: List of text chunks
        use_tokens: Whether to analyze by tokens instead of characters
    
    Returns:
        Dictionary of statistics
    """
    stats = {}
    
    # Basic statistics
    stats["num_chunks"] = len(chunks)
    
    if use_tokens:
        encoding = tiktoken.get_encoding("cl100k_base")
        chunk_sizes = [len(encoding.encode(chunk)) for chunk in chunks]
        stats["avg_size"] = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
        stats["min_size"] = min(chunk_sizes) if chunk_sizes else 0
        stats["max_size"] = max(chunk_sizes) if chunk_sizes else 0
        stats["size_unit"] = "tokens"
    else:
        chunk_sizes = [len(chunk) for chunk in chunks]
        stats["avg_size"] = sum(chunk_sizes) / len(chunk_sizes) if chunk_sizes else 0
        stats["min_size"] = min(chunk_sizes) if chunk_sizes else 0
        stats["max_size"] = max(chunk_sizes) if chunk_sizes else 0
        stats["size_unit"] = "chars"
    
    # Size distribution
    bins = 10
    histogram, bin_edges = np.histogram(chunk_sizes, bins=bins)
    stats["size_histogram"] = {
        "counts": histogram.tolist(),
        "bin_edges": bin_edges.tolist()
    }
    
    # Overlaps
    if len(chunks) >= 2:
        overlap_count = 0
        overlap_sizes = []
        
        for i in range(len(chunks) - 1):
            for j in range(i + 1, len(chunks)):
                chunk1, chunk2 = chunks[i], chunks[j]
                
                # Find longest common substring
                if use_tokens:
                    encoding = tiktoken.get_encoding("cl100k_base")
                    tokens1 = encoding.encode(chunk1)
                    tokens2 = encoding.encode(chunk2)
                    
                    max_overlap = 0
                    for start in range(len(tokens1)):
                        for length in range(1, len(tokens1) - start + 1):
                            if tokens1[start:start+length] in [tokens2[i:i+length] for i in range(len(tokens2) - length + 1)]:
                                max_overlap = max(max_overlap, length)
                    
                    if max_overlap > 0:
                        overlap_count += 1
                        overlap_sizes.append(max_overlap)
                else:
                    # Simple character-based overlap detection
                    max_overlap = 0
                    for length in range(1, min(len(chunk1), len(chunk2)) + 1):
                        if chunk1[-length:] == chunk2[:length] or chunk2[-length:] == chunk1[:length]:
                            max_overlap = max(max_overlap, length)
                    
                    if max_overlap > 10:  # Only count non-trivial overlaps
                        overlap_count += 1
                        overlap_sizes.append(max_overlap)
        
        stats["overlap_count"] = overlap_count
        stats["avg_overlap_size"] = sum(overlap_sizes) / len(overlap_sizes) if overlap_sizes else 0
    else:
        stats["overlap_count"] = 0
        stats["avg_overlap_size"] = 0
    
    return stats

def plot_chunk_stats(stats, title="Chunk Statistics", output_path="chunk_stats.png", strategy_name=None):
    """
    Create a visualization of chunk statistics.
    
    Args:
        stats: Dictionary of chunk statistics
        title: Title for the plot
        output_path: Path to save the plot
        strategy_name: Name of the chunking strategy for output directory organization
        
    Returns:
        Path to the generated plot
    """
    # Handle output directory based on strategy name
    if strategy_name:
        # Create strategy directory if it doesn't exist
        strategy_dir = os.path.join("output", strategy_name)
        os.makedirs(strategy_dir, exist_ok=True)
        
        # Update output path to be in the strategy directory
        filename = os.path.basename(output_path)
        output_path = os.path.join(strategy_dir, filename)
    
    plt.figure(figsize=(12, 8))
    
    # Size distribution histogram
    plt.subplot(2, 2, 1)
    bin_edges = stats["size_histogram"]["bin_edges"]
    bin_centers = [(bin_edges[i] + bin_edges[i+1])/2 for i in range(len(bin_edges)-1)]
    plt.bar(bin_centers, stats["size_histogram"]["counts"], width=(bin_edges[1]-bin_edges[0])*0.8)
    plt.title(f"Chunk Size Distribution ({stats['size_unit']})")
    plt.xlabel(f"Chunk Size ({stats['size_unit']})")
    plt.ylabel("Frequency")
    
    # Key metrics
    plt.subplot(2, 2, 2)
    metrics = ['avg_size', 'min_size', 'max_size']
    values = [stats[m] for m in metrics]
    labels = ['Average Size', 'Min Size', 'Max Size']
    plt.bar(labels, values, color=['blue', 'green', 'red'])
    plt.title(f"Chunk Size Metrics ({stats['size_unit']})")
    plt.ylabel(f"Size ({stats['size_unit']})")
    
    # Overlap information if available
    plt.subplot(2, 2, 3)
    plt.bar(['Number of Chunks', 'Overlap Count'], [stats['num_chunks'], stats['overlap_count']])
    plt.title("Chunk and Overlap Counts")
    
    # Add a text summary
    plt.subplot(2, 2, 4)
    summary = (
        f"Chunking Statistics Summary\n\n"
        f"Total Chunks: {stats['num_chunks']}\n"
        f"Average Size: {stats['avg_size']:.1f} {stats['size_unit']}\n"
        f"Size Range: {stats['min_size']} - {stats['max_size']} {stats['size_unit']}\n"
        f"Overlaps Detected: {stats['overlap_count']}\n"
        f"Avg Overlap Size: {stats['avg_overlap_size']:.1f} {stats['size_unit']}"
    )
    plt.text(0.5, 0.5, summary, ha='center', va='center', fontsize=10)
    plt.axis('off')
    
    plt.suptitle(title, fontsize=16)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(output_path)
    
    return output_path

def setup_chunking_output(strategy_name):
    """
    Create and set up output directory for a chunking strategy.
    
    Args:
        strategy_name: Name of the chunking strategy
        
    Returns:
        Path to the output directory
    """
    # Create base output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)
    
    # Create strategy directory if it doesn't exist
    strategy_dir = os.path.join("output", strategy_name)
    os.makedirs(strategy_dir, exist_ok=True)
    
    return strategy_dir

if __name__ == "__main__":
    # Example usage
    print("Chunk Visualizer - Example Usage:")
    print("from chunk_visualizer import visualize_chunks_html, analyze_chunks_stats, plot_chunk_stats, save_chunks_to_json, setup_chunking_output")
    print("output_dir = setup_chunking_output('character_chunking')")
    print("visualize_chunks_html(document, chunks, output_path=os.path.join(output_dir, 'visualization.html'), strategy_name='character_chunking')")
    print("save_chunks_to_json(chunks, 'character_chunking')")
