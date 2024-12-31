import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
def load_data(file_path):
    """Load the cleaned dataset."""
    return pd.read_csv(file_path)

# Analyze product return trends
def product_return_trends_analysis(df):
    """Analyze return rates for products and marketplaces."""
    # Ensure necessary columns exist
    required_columns = ["Parent ASIN", "Amazon store", "Units sold", "Units returned"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Calculate return rates by product
    product_return_rates = df.groupby("Parent ASIN")[["Units sold", "Units returned"]].sum().reset_index()
    product_return_rates["Return rate"] = (product_return_rates["Units returned"] / product_return_rates["Units sold"]) * 100
    product_return_rates = product_return_rates.sort_values(by="Return rate", ascending=False)

    print("\nProduct Return Rates:")
    print(product_return_rates.head(10))  # Display top 10 products with the highest return rates

    # Calculate return rates by marketplace
    marketplace_return_rates = df.groupby("Amazon store")[["Units sold", "Units returned"]].sum().reset_index()
    marketplace_return_rates["Return rate"] = (marketplace_return_rates["Units returned"] / marketplace_return_rates["Units sold"]) * 100
    marketplace_return_rates = marketplace_return_rates.sort_values(by="Return rate", ascending=False)

    print("\nMarketplace Return Rates:")
    print(marketplace_return_rates)

    # Visualization 1: Top 10 Products with Highest Return Rates
    top_10_products = product_return_rates.head(10)
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10_products, x="Parent ASIN", y="Return rate", palette="Reds")
    plt.title("Top 10 Products with Highest Return Rates")
    plt.ylabel("Return Rate (%)")
    plt.xlabel("Parent ASIN")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Visualization 2: Return Rates by Marketplace
    plt.figure(figsize=(12, 6))
    sns.barplot(data=marketplace_return_rates, x="Amazon store", y="Return rate", palette="Blues")
    plt.title("Return Rates by Marketplace")
    plt.ylabel("Return Rate (%)")
    plt.xlabel("Amazon Store")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Visualization 3: Units Sold vs. Units Returned (for Top 10 Products by Return Rate)
    plt.figure(figsize=(12, 6))
    top_10_products = top_10_products.melt(id_vars=["Parent ASIN"], value_vars=["Units sold", "Units returned"], 
                                           var_name="Metric", value_name="Count")
    sns.barplot(data=top_10_products, x="Parent ASIN", y="Count", hue="Metric", palette="muted")
    plt.title("Units Sold vs. Units Returned (Top 10 Products by Return Rate)")
    plt.ylabel("Count")
    plt.xlabel("Parent ASIN")
    plt.xticks(rotation=45)
    plt.legend(title="Metric")
    plt.tight_layout()
    plt.show()

# Main execution
def main():
    file_path = "cleaned_data.csv" 

    print("Loading data...")
    df = load_data(file_path)

    print("Analyzing product return trends...")
    product_return_trends_analysis(df)

if __name__ == "__main__":
    main()
