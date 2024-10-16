import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

def visualize_group_totals(group_totals):
    an_total = group_totals.get("AN", 0)
    se_total = group_totals.get("SE", 0)
    other_groups = {group: total for group, total in group_totals.items() if group not in ["AN", "SE"]}
    
    # Prepare data for plotting
    labels = ['Other Groups']
    other_totals = [sum(other_groups.values())]  # Sum of other groups
    
    # Create figure and axis
    plt.figure(figsize=(10, 6))

    # Plotting the first part (other groups)
    plt.bar(labels, other_totals, color='grey', label='Other Groups')

    # Stacking "AN" and "SE" on top of the "Other Groups" bar
    plt.bar(labels, [an_total], bottom=other_totals, color='blue', label='AN')
    plt.bar(labels, [se_total], bottom=[an_total + sum(other_totals)], color='orange', label='SE')

    # Customize the plot
    plt.title('Stacked Group Totals')
    plt.xlabel('Groups')
    plt.ylabel('Total Amount')
    plt.legend()  # Show the legend
    plt.xticks(rotation=45)

    # Save the plot to a file
    plt.savefig('/home/adi/cash/output/stacked_group_totals_chart.png')
    print("Stacked chart saved to /home/adi/cash/output/stacked_group_totals_chart.png")
    plt.close()  # Close the plot to free up resources
