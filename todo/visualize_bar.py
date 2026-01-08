import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

def visualize_group_totals(group_totals):
    an_total = group_totals.get("AN", 0)
    se_total = group_totals.get("SE", 0)
    other_groups = {group: total for group, total in group_totals.items() if group not in ["AN", "SE"]}
    
    # Prepare data for plotting
    labels = ['AN', 'SE'] + list(other_groups.keys())
    totals = [an_total, se_total] + list(other_groups.values())
    
    # Plotting bar chart instead of pie chart
    plt.figure(figsize=(10, 6))
    plt.bar(labels, totals, color=['blue', 'orange'] + ['grey'] * len(other_groups))
    plt.title('Group Totals')
    plt.xlabel('Groups')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45)
    
    # Save the plot to a file
    plt.savefig('/home/adi/cash/output/group_totals_chart.png')
    print("Chart saved to /home/adi/cash/output/group_totals_chart.png")
    plt.close()  # Close the plot to free up resources
