import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
def load_data(file_path):
    """Load the cleaned dataset."""
    return pd.read_csv(file_path)

# Analyze profitability
def profitability_analysis(df):
    """Perform profitability analysis and visualizations."""
    # Ensure necessary columns exist
    required_columns = ["Parent ASIN", "Net proceeds total", "Net sales", "Units sold"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Calculate profitability metrics
    profitability_summary = df.groupby("Parent ASIN")[["Net proceeds total", "Net sales", "Units sold"]].sum().reset_index()

    # Add profitability ratio: Net Proceeds to Net Sales
    profitability_summary["Profitability ratio"] = profitability_summary["Net proceeds total"] / profitability_summary["Net sales"]

    # Sort by Net Proceeds Total
    profitability_summary = profitability_summary.sort_values(by="Net proceeds total", ascending=False)

    print("\nProfitability Summary:")
    print(profitability_summary)

    # Visualization 1: Top 10 Products by Net Proceeds
    top_10_products = profitability_summary.head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10_products, x="Parent ASIN", y="Net proceeds total", palette="viridis")
    plt.title("Top 10 Products by Net Proceeds")
    plt.ylabel("Net Proceeds Total")
    plt.xlabel("Parent ASIN")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Visualization 2: Profitability Ratio by Top 10 Products
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10_products, x="Parent ASIN", y="Profitability ratio", palette="coolwarm")
    plt.title("Profitability Ratio of Top 10 Products")
    plt.ylabel("Profitability Ratio")
    plt.xlabel("Parent ASIN")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main execution
def main():
    file_path = "cleaned_data.csv"

    print("Loading data...")
    df = load_data(file_path)

    print("Analyzing profitability...")
    profitability_analysis(df)

if __name__ == "__main__":
    main()
