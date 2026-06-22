# Amazon Executive Sales Maximization Dashboard

#### Link: https://executivesalesdashboard-rm6ftciyk7rhdukq5vm5pd.streamlit.app/

A business intelligence application and automated data analytics pipeline built using Python, Pandas, and Streamlit. This application translates raw, unformatted Amazon marketplace transaction logs into strategic pricing strategies and inventory optimization directives for enterprise vendor managers.

## Business Objectives & Solved Problems

Enterprise e-commerce operations managing thousands of SKUs face severe revenue leakage due to unoptimized pricing loops and poor catalog visibility. This application solves three core operational friction points:

1. **Eliminating CRaP (Can't Realize a Profit) Inventory**: Automatically flags high-discount items that suffer from poor customer satisfaction ratings, allowing management to halt margin erosion.
2. **Unlocking Hidden Demand**: Identifies "Undiscovered Gems"—products with high buyer satisfaction ratings but low overall market visibility—ready for immediate promotional acceleration.
3. **Locating the Discount Sweet Spot**: Mathematically calculates the exact markdown tier where conversion velocity triggers maximum Gross Merchandise Value (GMV), preventing over-discounting.

---

## Technical Architecture & Pipeline Strategy
### 1. Data Engineering Pipeline (ETL)
Raw marketplace data contains messy formatting (currency indicators, embedded strings, and alphanumeric notation) that prevent statistical modeling. The application runs an automated data transformation layer upon ingestion:
* **Numeric Sanitization**: Regular expression stripping applied to currency formats and percentage symbols, converting text variables safely into standard floating-point numbers.
* **Structural Token Splitting**: Hierarchical category text paths (e.g., `Electronics|Accessories|Cables`) are parsed programmatically using token splitting to isolate the high-level root category.
* **Analytic Proxy Calculation**: Generates a weighted economic value proxy metric (`revenue_proxy = discounted_price * rating_count`) to track estimated transaction velocity patterns without absolute sales data.

### 2. High-Utility Visual Analytics Matrix
The application moves beyond simple tracker lines and incorporates advanced multi-dimensional visualization charts:
* **Pricing Elasticity Sweet-Spot Locator**: A segmented trend timeline mapping customer conversion value relative to specific markdown percentages.
* **Top 10 Product Sales Leaderboard**: A horizontal bar ranking matrix that programmatically truncates complex item descriptions to ensure corporate visual layout clarity.
* **Promotion Strategy Heatmap Matrix**: An aggregated density grid crossing customer satisfaction tiers against applied discounts, identifying market concentration hotspots instantly.

---
## Project Structure

```text
├── app.py                  # Monolithic web application, layout layer, and data pipeline
├── requirements.txt        # Managed Python environment dependencies
└── amazon.csv              # Raw Amazon catalog transactional dataset (Kaggle Source)
```

---

## Installation & Local Execution

### Prerequisites
Ensure that Python 3.10 or higher is installed and properly mapped to your local system terminal variables.

### 1. Clone or Initialize the Workspace
Create a folder directory on your local machine and place the configuration files inside it:
```bash
mkdir amazon-sales-dashboard
cd amazon-sales-dashboard
```

### 2. Install Package Dependencies
Install the required engineering libraries using the provided requirements file:
```bash
python -m pip install -r requirements.txt
```

### 3. Launch the Streamlit Engine
Execute the script explicitly as a system module to fire up the native localhost server:
```bash
python -m streamlit run app.py
```
Once executed, a browser tab window will automatically populate at `http://localhost:8501`.

---
## Core Dependencies Matrix

The project environment is controlled and locked down using the following target versions inside `requirements.txt`:

```text
streamlit>=1.35.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.15.0
openpyxl>=3.1.0
```

---

## User Interface & Strategic Walkthrough

1. **Dashboard Controls (Sidebar)**: Utilizes a dynamic multi-select widget allowing users to filter analytics by one or multiple product categories.
2. **Actionable Analytics (KPI Row)**: Displays catalog GMV values, item counts for hidden gems, underperforming items, and promotional candidates.
3. **Strategic Action Plan**: Converts mathematical data relationships directly into plain-English tactical directives for inventory allocation and marketing spend.
4. **Granular Exploration Tabs**: Combines an interactive product spreadsheet list (featuring a direct native CSV data exporter tool) and advanced visual analysis charts into separate tabs to minimize cognitive clutter.
