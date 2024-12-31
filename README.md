# Data Scientist Technical Challenge Part 2

This repository contains files for the **Data Scientist Technical Challenge Part 2**, which involves extracting, cleaning, and analyzing complex data. The project demonstrates expertise in handling nested JSON data, transforming it into a usable format, and performing advanced analyses.

## **Project Overview**

### **1. Data Extraction and Cleaning**
The script `extract_clean_data.py` is designed to extract data from the complex JSON file `dummydata.txt` and clean it into a structured CSV file named `cleaned_data.csv`.

#### Key Features:
- **Hybrid Approach for Handling Mismatched Column Names:**
  - **Field Mapping Tables**: Explicit mappings for known fields.
  - **Dynamic JSON Flattening**: Handles nested JSON structures.
  - **Fuzzy Matching**: Matches inexact or inconsistent column names to target fields.
- The resulting cleaned data is saved in the file `cleaned_data.csv` for further analysis.

### **2. Bonus Analyses**
The `bonus_analysis` folder contains Python scripts for various analytical tasks based on the cleaned data:

#### **a. Anomaly Detection**
File: `anomaly_detection.py`
- Identifies unusual spikes or drops in key metrics such as `Net sales`, `Units sold`, and `Units returned`.
- Detects negative or missing values in critical fields (e.g., `Net sales`, `Units sold`).
- Includes time-series visualizations to highlight anomalies.

#### **b. Product Return Trends**
File: `product_return_trends.py`
- Calculates the return rates for each product (`Parent ASIN`) and marketplace (`Amazon store`).
- Identifies products or marketplaces with unusually high return rates.
- Provides visualizations for:
  - Top 10 products with the highest return rates.
  - Return rates by marketplace.
  - Comparison of `Units sold` vs. `Units returned` for high-return products.

#### **c. Profitability Analysis**
File: `profitability_analysis.py`
- Highlights products or categories generating the highest `Net proceeds`.
- Computes profitability ratios (`Net proceeds total / Net sales`) to evaluate performance.
- Visualizations include:
  - Top 10 products by `Net proceeds`.
  - Profitability ratios of top-performing products.

## **How to Run the Project**

### **1. Prerequisites**
- Python 3.7+
- Required Python libraries:
  - `pandas`
  - `numpy`
  - `matplotlib`
  - `seaborn`
  - `fuzzywuzzy`

Install the required libraries using:
```bash
pip install pandas numpy matplotlib seaborn fuzzywuzzy
```

### **2. Data Extraction and Cleaning**
Run the `extract_clean_data.py` script to extract and clean the data from `dummydata.txt`:
```bash
python extract_clean_data.py
```
This will generate the cleaned dataset as `cleaned_data.csv`.

### **3. Bonus Analyses**
Navigate to the `bonus_analysis` folder and run any of the following scripts:

#### Anomaly Detection:
```bash
python anomaly_detection.py
```
#### Product Return Trends:
```bash
python product_return_trends.py
```
#### Profitability Analysis:
```bash
python profitability_analysis.py
```

Each script will display a detailed analysis with printed DataFrames and visualizations.

## **Project Structure**
```
.
├── dummydata.txt               # Input file containing the complex JSON data
├── cleaned_data.csv            # Cleaned data generated after extraction
├── extract_clean_data.py       # Script for extracting and cleaning the data
├── bonus_analysis/             # Folder containing analysis scripts
│   ├── anomaly_detection.py    # Script for anomaly detection
│   ├── product_return_trends.py# Script for product return trends
│   └── profitability_analysis.py# Script for profitability analysis
├── README.md                   # Project documentation
```
