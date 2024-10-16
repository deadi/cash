import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

def visualize_earnings_vs_spendings(group_totals):
    earnings = {group: total for group, total in group_totals.items() if total > 0}
    spendings = {group: total for group, total in group_totals.items() if total < 0}

    groups = list(group_totals.keys())
    
    # Prepare earnings and spendings values for each group
    earnings_values = [earnings.get(group, 0) for group in groups]
    spendings_values = [spendings.get(group, 0) for group in groups]

    # Set up the plot
    plt.figure(figsize=(12, 7))

    # Plot earnings as positive bars
    plt.bar(groups, earnings_values, color='green', label='Earnings')

    # Plot spendings as negative bars (absolute values for bars)
    plt.bar(groups, spendings_values, color='red', label='Spendings')

    # Customize the plot
    plt.title('Earnings vs Spendings by Group')
    plt.xlabel('Groups')
    plt.ylabel('Amount')
    plt.xticks(rotation=45)
    plt.legend()  # Show the legend to differentiate earnings and spendings

    # Save the plot to a file
    plt.savefig('/home/adi/cash/output/earnings_vs_spendings_chart.png')
    print("Earnings vs Spendings chart saved to /home/adi/cash/output/earnings_vs_spendings_chart.png")
    plt.close()  # Close the plot to free up resources
