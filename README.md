# PortaOne Test: Finding the maximum chain of numbers

A web application and CLI utility for quickly finding the longest chain where the end of one number matches the beginning of another (2-character overlap).

### 🔗 Live Demo
* **Web App (Streamlit Cloud):** [portaonetest.streamlit.app](https://portaonetest-3zcfvz56jsdwgbcgs6y4wf.streamlit.app)

---

## 🚀 How It Works (Algorithm & Optimizations)

The algorithm is optimized to process large data sets (up to 10,000+ elements) without freezing.

1. **Overlap Graph Construction:** The numbers are modeled as a directed graph. The 2-digit prefixes and suffixes represent the nodes (vertices), while the actual fragments act as directed edges.
2. **Heuristic Start-Node Selection:** Instead of brute-forcing paths from every single vertex, the algorithm ranks nodes by their degree difference ($OutDegree - InDegree$). This quickly identifies "sources"—the most mathematically optimal starting points of a chain.
3. **Optimized Eulerian Trail-like Search:** The search utilizes **Beam Search** (limiting the search branching factor to the top-4 unique routes) combined with **Memoization** (caching visited subpaths). This eliminates redundant computations on deep, complex branches and completely avoids combinatorial explosion.

---

## 💻 Local CLI Execution (Pure Python)

The console-based execution pipeline (`main_app.py`) is written in **pure Python** and does not require any external dependencies.

### Prerequisites
* **Python 3.12** or higher.

### Quick Start:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Alexey-Goryachev/portaone_test.git
   cd portaone_test
   ```
2. **Run the script:**

   On Linux / macOS:

   ```bash
   ./run.sh
   (Or run directly: python3 main_app.py)
   ```
   On Windows:
   Double-click the run.bat file, or run it via command line:

   ```cmd￼
   run.bat
   (Or run directly: python main_app.py)
   ```
3. **🌐 Local Web App Execution (Poetry)**
   If you want to run the interactive Streamlit UI locally, use the Poetry package manager:

   Install dependencies:

   ```bash
   poetry install
   ```
   Run the Streamlit server:

   ```bash
   poetry run streamlit run web_app.py
   ```
