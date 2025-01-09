import json # Parsed JSON data from the file and handle any potential JSON decoding issues.
import pandas as pd # Creating and manipulating structured data in the form of DataFrames to simplify data analysis.
import numpy as np # Handling missing values by assigning NaN to unspecifided columns.
from fuzzywuzzy import process # Fuzzy matching between raw keys and target column names, enabling approximate string matching.

# Load and Parse the File
def load_data(file_path):
    """
    Reads the data from the specified file and parses it line by line.
    Assumes each line in the file is a valid JSON object.

    Parameters:
        file_path (str): Path to the file containing JSON data.

    Returns:
        list: A list of parsed JSON objects.
    """
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            try:
                parsed_line = json.loads(line.strip())
                data.append(parsed_line)
            except json.JSONDecodeError:
                print(f"Skipping invalid line: {line}")
    return data

# Define Hybrid Mapping Approach
# Field mapping table for exact matches
field_mapping = {
    "marketplaceId": "Amazon store",
    "startDate": "Start date",
    "endDate": "End date",
    "parentAsin": "Parent ASIN",
    "childAsin": "ASIN",
    "fnsku": "FNSKU",
    "msku": "MSKU",
    "netProceeds.perUnit.currencyCode": "Currency code",
    "sales.averageSellingPrice.amount": "Average sales price",
    "sales.unitsOrdered": "Units sold",
    "sales.unitsRefunded": "Units returned",
    "sales.netUnitsSold": "Net units sold",
    "sales.orderedProductSales.amount": "Sales",
    "sales.netProductSales.amount": "Net sales",
    "fees.baseFulfillment.perUnit": "Base fulfilment fee per unit",
    "fees.baseFulfillment.quantity": "Base fulfilment fee quantity",
    "fees.baseFulfillment.total": "Base fulfilment fee total",
    "cost.costOfGoodsSold": "Cost of goods sold per unit",
    "cost.miscellaneousCost": "Miscellaneous cost per unit",
    "netProceeds.total.amount": "Net proceeds total",
}

# Target columns for the DataFrame
target_columns = [
    "Amazon store", "Start date", "End date", "Parent ASIN", "ASIN",
    "FNSKU", "MSKU", "Currency code", "Average sales price", "Units sold",
    "Units returned", "Net units sold", "Sales", "Net sales",
    "Base fulfilment fee per unit", "Base fulfilment fee quantity",
    "Base fulfilment fee total", "Fulfilment by Amazon fulfilment fees per unit",
    "Fulfilment by Amazon fulfilment fees quantity", "Fulfilment by Amazon fulfilment fees total",
    "Inbound Transportation Program Fee per unit", "Inbound Transportation Program Fee quantity",
    "Inbound Transportation Program Fee total", "Inbound transportation charge per unit",
    "Inbound transportation charge quantity", "Inbound transportation charge total",
    "Low-inventory-level fee per unit", "Low-inventory-level fee quantity",
    "Low-inventory-level fee total", "Referral fee per unit", "Referral fee quantity",
    "Referral fee total", "Refund administration fee per unit", "Refund administration fee quantity",
    "Refund administration fee total", "Sponsored Products charge per unit",
    "Sponsored Products charge quantity", "Sponsored Products charge total",
    "Cost of goods sold per unit", "Miscellaneous cost per unit", "Net proceeds total",
    "Net proceeds per unit"
]

# Fuzzy matching for inexact matches
def fuzzy_map_key(raw_key, target_columns, threshold=80):
    """
    Maps a raw key to the closest target column using fuzzy string matching.

    Parameters:
        raw_key (str): The raw key to match.
        target_columns (list): List of target column names.
        threshold (int): Minimum match score to consider a match (default is 80).

    Returns:
        str or None: The best match if the score exceeds the threshold, otherwise None.
    """
    best_match, score = process.extractOne(raw_key, target_columns)
    return best_match if score >= threshold else None

# Flatten nested JSON dynamically
def flatten_json(json_obj, parent_key='', sep='.'):
    """
    Flattens a nested JSON object into a single-level dictionary.

    Parameters:
        json_obj (dict): The JSON object to flatten.
        parent_key (str): Prefix for the keys (used for recursion).
        sep (str): Separator to use for flattened keys (default is '.').

    Returns:
        dict: A flattened dictionary.
    """
    items = []
    for key, value in json_obj.items():
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):
            items.extend(flatten_json(value, new_key, sep=sep).items())
        else:
            items.append((new_key, value))
    return dict(items)

# Map Fields to Target Columns
def map_to_dataframe(raw_data):
    """
    Maps raw JSON data to a structured DataFrame format with specified columns.
    Handles both exact and fuzzy mapping of fields.

    Parameters:
        raw_data (list): List of raw JSON objects.

    Returns:
        pd.DataFrame: A DataFrame with cleaned and structured data.
    """
    processed_data = []
    for record in raw_data:
        # Flatten the record
        flattened_record = flatten_json(record)

        # Map fields using exact matches and fuzzy matching
        row = {}
        for raw_key, raw_value in flattened_record.items():
            if raw_key in field_mapping:
                row[field_mapping[raw_key]] = raw_value
            else:
                fuzzy_matched_column = fuzzy_map_key(raw_key, target_columns)
                if fuzzy_matched_column:
                    row[fuzzy_matched_column] = raw_value

        # Add missing columns as NaN
        for column in target_columns:
            if column not in row:
                row[column] = np.nan

        processed_data.append(row)

    # Create DataFrame
    df = pd.DataFrame(processed_data, columns=target_columns)
    return df

# Simple Analysis
def analyze_data(df):
    """
    Perform basic analysis on the cleaned data to identify patterns or insights.

    Parameters:
        df (pd.DataFrame): The cleaned DataFrame.

    Examples:
        - Summarizes sales by Amazon store.
        - Identifies the top 5 products by net sales.
    """
    # Example: Summarize sales by Amazon store
    summary = df.groupby("Amazon store")["Net sales"].sum()
    print("\nSales Summary by Amazon Store:")
    print(summary)

    # Example: Identify top 5 products by sales
    top_products = df.nlargest(5, "Net sales", "all")
    print("\nTop 5 Products by Net Sales:")
    print(top_products[["Parent ASIN", "ASIN", "Net sales"]])

# Main Execution
def main():
    """
    Main function to load data, process it, and perform analysis.

    Steps:
        1. Load raw JSON data from the file.
        2. Map the data to a structured DataFrame.
        3. Display and save the cleaned DataFrame.
        4. Perform basic data analysis.
    """
    file_path = "dummydata.txt"  # Path to the input file

    print("Loading data...")
    raw_data = load_data(file_path)

    print("Mapping data to DataFrame...")
    df = map_to_dataframe(raw_data)

    print("\nCleaned DataFrame:")
    print(df.head())

    # Save DataFrame to CSV
    df.to_csv("cleaned_data.csv", index=False)

    # Perform bonus analysis
    analyze_data(df)

if __name__ == "__main__":
    main()
