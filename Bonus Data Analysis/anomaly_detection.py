import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the cleaned data
def load_data(file_path):
    """Load the cleaned dataset."""
    return pd.read_csv(file_path)

# Perform anomaly detection
def anomaly_detection_analysis(df):
    """Analyze the data for anomalies and unusual patterns."""
    # Ensure necessary columns exist
    required_columns = ["Start date", "Net sales", "Units sold", "Units returned"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    # Convert 'Start date' to datetime for time series analysis
    df["Start date"] = pd.to_datetime(df["Start date"], errors='coerce')

    # Identify unusual spikes or drops in sales, fees, or returns
    metrics = ["Net sales", "Units sold", "Units returned"]
    anomalies = {}

    for metric in metrics:
        # Rolling mean and standard deviation for anomaly detection
        df[f"{metric} rolling mean"] = df[metric].rolling(window=7, min_periods=1).mean()
        df[f"{metric} rolling std"] = df[metric].rolling(window=7, min_periods=1).std()

        # Identify anomalies as points outside 3 standard deviations
        df[f"{metric} anomaly"] = abs(df[metric] - df[f"{metric} rolling mean"]) > (3 * df[f"{metric} rolling std"])
        anomalies[metric] = df[df[f"{metric} anomaly"]]

        # Visualization of time series with anomalies
        plt.figure(figsize=(12, 6))
        plt.plot(df["Start date"], df[metric], label=metric, alpha=0.7)
        plt.plot(df["Start date"], df[f"{metric} rolling mean"], label=f"{metric} Rolling Mean", linestyle="--", alpha=0.8)
        plt.scatter(anomalies[metric]["Start date"], anomalies[metric][metric], color="red", label="Anomalies", zorder=5)
        plt.title(f"Anomaly Detection for {metric}")
        plt.ylabel(metric)
        plt.xlabel("Date")
        plt.legend()
        plt.tight_layout()
        plt.show()

    # Check for negative or missing values in critical fields
    critical_fields = ["Net sales", "Units sold", "Units returned"]
    negative_values = {}
    missing_values = {}

    for field in critical_fields:
        negative_values[field] = df[df[field] < 0]
        missing_values[field] = df[df[field].isnull()]

        print(f"\nNegative values in {field}:")
        print(negative_values[field])

        print(f"\nMissing values in {field}:")
        print(missing_values[field])

    return anomalies, negative_values, missing_values

# Main execution
def main():
    file_path = "cleaned_data.csv"

    print("Loading data...")
    df = load_data(file_path)

    print("Analyzing anomalies...")
    anomalies, negative_values, missing_values = anomaly_detection_analysis(df)

if __name__ == "__main__":
    main()
