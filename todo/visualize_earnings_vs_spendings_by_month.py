import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

def visualize_earnings_vs_spendings_by_month(transactions, date_column='date', amount_column='amount'):
    # Convert transactions into a DataFrame (assuming transactions is a list of dictionaries or similar)
    df = pd.DataFrame(transactions)
    
    # Convert date column to datetime format
    df[date_column] = pd.to_datetime(df[date_column])
    
    # Extract month-year (e.g., '2024-09') for grouping
    df['month'] = df[date_column].dt.to_period('M')

    # Group data by month and calculate earnings (positive) and spendings (negative) totals
    monthly_totals = df.groupby('month')[amount_column].agg(
        earnings=lambda x: x[x > 0].sum(), 
        spendings=lambda x: x[x < 0].sum()
    ).reset_index()

    # Prepare the data for plotting
    months = monthly_totals['month'].astype(str)  # Convert to string for better plotting
    earnings = monthly_totals['earnings']
    spendings = monthly_totals['spendings'].abs()  # Take absolute value of spendings for stacked bars

    # Plot stacked bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(months, earnings, label='Earnings', color='green')
    plt.bar(months, spendings, bottom=earnings, label='Spendings', color='red')

    # Customize the plot
    plt.title('Earnings vs Spendings Over Time (Monthly)')
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend()

    # Save the plot to a file
    plt.savefig('/home/adi/cash/output/earnings_vs_spendings_by_month_chart.png')
    print("Earnings vs Spendings by Month chart saved to /home/adi/cash/output/earnings_vs_spendings_by_month_chart.png")
    plt.close()  # Close the plot to free up resources
