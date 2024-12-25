#Importing csv files to make the figures

# Cell 1: Import libraries and read data
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
# Read the data
nba_03 = pd.read_csv('NBA_03.csv')
nba_13 = pd.read_csv('nba_13.csv')
nba_23 = pd.read_csv('NBA_23.csv')
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size'] = 12
# Cell 2: Calculate averages
averages = {
    '2003/04': {
        'pts': nba_03['PTS'].mean(),
        'threePtAttempts': nba_03['3PA'].mean(),
        'threePtPercentage': nba_03['3P%'].mean() * 100
    },
    '2013/14': {
        'pts': nba_13['PTS'].mean(),
        'threePtAttempts': nba_13['3PA'].mean(),
        'threePtPercentage': nba_13['3P%'].mean() * 100
    },
    '2023/24': {
        'pts': nba_23['PTS'].mean(),
        'threePtAttempts': nba_23['3PA'].mean(),
        'threePtPercentage': nba_23['3P%'].mean() * 100
    }
}
# Create DataFrame for plotting
df_averages = pd.DataFrame(averages).T
# Cell 1: Prepare the data
# Add a 'Year' column to each dataframe
nba_03['Year'] = '2003/04'
nba_13['Year'] = '2013/14'
nba_23['Year'] = '2023/24'
# Combine all datasets
combined_df = pd.concat([nba_03, nba_13, nba_23])
# Cell 2: Create scatter plot with contrasting colors and shapes
plt.figure(figsize=(12, 8))
# Define vibrant contrasting colors and markers
style_dict = {
    '2003/04': {'color': '#FF0000', 'marker': 'o'},     # Bright Red, circles
    '2013/14': {'color': '#4B0082', 'marker': 's'},     # Indigo, squares
    '2023/24': {'color': '#1E90FF', 'marker': '^'}      # Bright Blue, triangles
}
# Remove default grid
sns.set_style("white")
# Create scatter plot with enhanced styling
for year, style in style_dict.items():
    year_data = combined_df[combined_df['Year'] == year]

    # Plot scatter points
    plt.scatter(year_data['3PA'], year_data['PTS'], 
                c=style['color'], 
                marker=style['marker'],
                label=year,
                alpha=0.8,
                s=150,
                edgecolor='white',
                linewidth=1)

    # Add trend line
    z = np.polyfit(year_data['3PA'], year_data['PTS'], 1)
    p = np.poly1d(z)
    x_trend = np.linspace(year_data['3PA'].min(), year_data['3PA'].max(), 100)
    plt.plot(x_trend, p(x_trend), '--', color=style['color'], 
             alpha=0.8, linewidth=2)
# Style the plot
plt.title('Evolution of NBA Scoring and 3-Point Attempts', 
          fontsize=16, pad=20, fontweight='bold')
plt.xlabel('3-Point Attempts per Game', fontsize=12, fontweight='bold')
plt.ylabel('Points per Game', fontsize=12, fontweight='bold')
# Style the legend
legend = plt.legend(title='Season', title_fontsize=12, fontsize=10,
                   frameon=True, edgecolor='black',
                   facecolor='white', framealpha=0.9,
                   loc='upper right',
                   markerscale=1.5)  # Make legend markers bigger
legend.get_frame().set_linewidth(1.5)
# Add correlation coefficients with matching colors
for i, (year, style) in enumerate(style_dict.items()):
    year_data = combined_df[combined_df['Year'] == year]
    corr = year_data['3PA'].corr(year_data['PTS']).round(3)
    plt.text(0.02, 0.98 - i*0.05, 
             f'{year} correlation: {corr}',
             transform=plt.gca().transAxes,
             color=style['color'],
             fontsize=10,
             fontweight='bold')
# Set background color
plt.gca().set_facecolor('white')
plt.gcf().set_facecolor('white')
# Add a light gray grid in the background
plt.grid(True, alpha=0.2, color='gray', linestyle='--')
plt.tight_layout()
plt.show()
