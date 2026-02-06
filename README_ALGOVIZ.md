# AlgoViz Pro - Production-Grade Algorithm Visualization Platform

A professional, enterprise-grade web platform for visualizing and exploring fundamental computer science algorithms.

## Features

### Three Powerful Modules

1. **Graph Coloring**
   - Welsh-Powell algorithm implementation
   - Automatic chromatic number calculation
   - Multiple coloring combinations visualization
   - Manual coloring mode

2. **Minimum Spanning Tree (MST)**
   - Prim's algorithm implementation
   - Weighted graph support
   - Visual MST edge highlighting
   - Total minimum weight calculation

3. **Huffman Coding**
   - Automatic frequency analysis
   - Binary code generation
   - Compression statistics
   - Visual frequency table

## Technology Stack

- **Backend**: Python 3.x with Flask
- **Visualization**: NetworkX, Matplotlib
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Icons**: FontAwesome
- **Fonts**: Google Fonts (Inter)

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install Flask==3.0.0 matplotlib==3.8.2 networkx==3.2.1
```

### 2. Run the Application

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`

## Project Structure

```
AlgoViz-Pro/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── static/
│   └── css/
│       └── style.css              # All styling (Enterprise SaaS theme)
└── templates/
    ├── layout.html                # Base template with sidebar & header
    ├── home.html                  # Dashboard
    ├── graph_coloring/            # Graph Coloring module templates
    │   ├── index.html
    │   ├── matrix.html
    │   ├── graph.html
    │   ├── chromatic_index.html
    │   ├── manual_color.html
    │   └── manual_color_result.html
    ├── mst/                       # MST module templates
    │   ├── index.html
    │   ├── matrix.html
    │   └── result.html
    └── huffman/                   # Huffman Coding module templates
        ├── index.html
        └── result.html
```

## Design System

### Color Palette
- **Primary**: Tech Blue (#2563eb)
- **Sidebar**: Dark Navy (#0f172a)
- **Background**: Light Gray (#f1f5f9)
- **Cards**: White (#ffffff)

### Typography
- **Font Family**: Inter (Google Fonts)
- **Line Height**: 150% for body, 120% for headings
- **Font Weights**: 300, 400, 500, 600, 700

### Components
- **Cards**: White with soft shadows (box-shadow: 0 1px 3px rgba(0,0,0,0.1))
- **Buttons**: Rounded with primary color
- **Sidebar**: Fixed, collapsible on mobile
- **Header**: Sticky with breadcrumbs

## Usage Guide

### Graph Coloring
1. Navigate to "Graph Coloring" from the sidebar
2. Enter the number of vertices (2-10)
3. Fill in the adjacency matrix (1 = connected, 0 = not connected)
4. Click "Visualize Graph" to see the graph structure
5. Click "Find Chromatic Number" to see colored versions

### Minimum Spanning Tree
1. Navigate to "MST Algorithm" from the sidebar
2. Enter the number of vertices (2-10)
3. Fill in the weighted adjacency matrix (0 = no connection, positive numbers = weight)
4. Click "Calculate MST" to see the result
5. Green edges indicate the MST, gray dashed edges are non-MST edges

### Huffman Coding
1. Navigate to "Huffman Coding" from the sidebar
2. Enter any text in the textarea
3. Click "Generate Huffman Codes"
4. View character frequencies and their binary codes
5. See compression statistics

## Key Algorithms

### Welsh-Powell Algorithm (Graph Coloring)
1. Sort vertices in descending order by degree
2. Assign the first available color to each vertex
3. Ensure no adjacent vertices share the same color

### Prim's Algorithm (MST)
1. Start with an arbitrary vertex
2. Repeatedly add the minimum weight edge connecting a vertex in the tree to one outside
3. Continue until all vertices are included

### Huffman Coding
1. Calculate character frequencies
2. Build a binary tree with characters as leaves
3. Assign codes: 0 for left branches, 1 for right branches
4. Generate unique prefix-free codes

## Responsive Design

The application is fully responsive:
- **Desktop**: Full sidebar visible
- **Tablet**: Collapsible sidebar
- **Mobile**: Hidden sidebar with toggle button

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Production Deployment

For production deployment:

1. Set Flask to production mode:
```python
app.run(debug=False, host='0.0.0.0', port=5000)
```

2. Use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

3. Set up a reverse proxy (Nginx recommended)

## License

This is a demonstration project for algorithm visualization.

## Credits

- **Algorithms**: Classic computer science algorithms
- **Visualization**: NetworkX and Matplotlib
- **UI Framework**: Custom CSS with Enterprise SaaS design principles
- **Icons**: FontAwesome
- **Fonts**: Google Fonts (Inter)
