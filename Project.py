import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def load_and_prepare_data(path_03, path_13, path_23):
    """Load and prepare NBA data from three seasons."""
    nba_03 = pd.read_csv(path_03)
    nba_13 = pd.read_csv(path_13)
    nba_23 = pd.read_csv(path_23)
    
    # Add Year columns
    nba_03['Year'] = nba_03['Season'] = '2003/04'
    nba_13['Year'] = nba_13['Season'] = '2013/14'
    nba_23['Year'] = nba_23['Season'] = '2023/24'
    
    combined_df = pd.concat([nba_03, nba_13, nba_23])
    
    return nba_03, nba_13, nba_23, combined_df

def calculate_shot_averages(nba_03, nba_13, nba_23):
    """Calculate average shot attempts for each season."""
    averages = {
        '2003/04': {
            '3PT Attempts': nba_03['3PA'].mean(),
            '2PT Attempts': nba_03['2PA'].mean(),
            'FT Attempts': nba_03['FTA'].mean()
        },
        '2013/14': {
            '3PT Attempts': nba_13['3PA'].mean(),
            '2PT Attempts': nba_13['2PA'].mean(),
            'FT Attempts': nba_13['FTA'].mean()
        },
        '2023/24': {
            '3PT Attempts': nba_23['3PA'].mean(),
            '2PT Attempts': nba_23['2PA'].mean(),
            'FT Attempts': nba_23['FTA'].mean()
        }
    }
    return pd.DataFrame(averages).T

def calculate_shot_percentage_changes(df_attempts):
    """Calculate percentage changes in shot attempts between first and last season."""
    changes = {}
    for shot_type in ['3PT Attempts', '2PT Attempts', 'FT Attempts']:
        change = ((df_attempts[shot_type].iloc[-1] - df_attempts[shot_type].iloc[0]) / 
                  df_attempts[shot_type].iloc[0] * 100)
        changes[shot_type] = change
    return changes

def create_scoring_attempts_plot(combined_df):
    """Create scatter plot of scoring vs 3-point attempts."""
    plt.figure(figsize=(12, 8))
    style_dict = {
        '2003/04': {'color': '#FF0000', 'marker': 'o'},
        '2013/14': {'color': '#4B0082', 'marker': 's'},
        '2023/24': {'color': '#1E90FF', 'marker': '^'}
    }
    
    for year, style in style_dict.items():
        year_data = combined_df[combined_df['Year'] == year]
        plt.scatter(year_data['3PA'], year_data['PTS'], 
                   c=style['color'], 
                   marker=style['marker'],
                   label=year,
                   alpha=0.8,
                   s=150,
                   edgecolor='white',
                   linewidth=1)
        
        z = np.polyfit(year_data['3PA'], year_data['PTS'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(year_data['3PA'].min(), year_data['3PA'].max(), 100)
        plt.plot(x_trend, p(x_trend), '--', color=style['color'], alpha=0.8, linewidth=2)
    
    plt.title('Evolution of NBA Scoring and 3-Point Attempts', 
              fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('3-Point Attempts per Game', fontsize=12, fontweight='bold')
    plt.ylabel('Points per Game', fontsize=12, fontweight='bold')
    plt.legend(title='Season', title_fontsize=12, fontsize=10,
              frameon=True, edgecolor='black',
              facecolor='white', framealpha=0.9)
    plt.grid(True, alpha=0.2, color='gray', linestyle='--')
    plt.tight_layout()
    return plt.gcf()

def create_shot_attempts_comparison(df_attempts):
    """Create bar plot comparing different shot attempts across seasons."""
    plt.figure(figsize=(12, 8))
    width = 0.25
    x = np.arange(len(df_attempts.index))

    plt.bar(x - width, df_attempts['3PT Attempts'], width, label='3PT Attempts', 
            color='#FF0000', alpha=0.8)
    plt.bar(x, df_attempts['2PT Attempts'], width, label='2PT Attempts', 
            color='#4B0082', alpha=0.8)
    plt.bar(x + width, df_attempts['FT Attempts'], width, label='FT Attempts', 
            color='#1E90FF', alpha=0.8)

    plt.title('Evolution of Shot Attempts in NBA (2003-2024)', 
              fontsize=16, pad=20, fontweight='bold')
    plt.xlabel('Season', fontsize=12, fontweight='bold')
    plt.ylabel('Average Attempts per Game', fontsize=12, fontweight='bold')
    plt.xticks(x, df_attempts.index, fontsize=10, fontweight='bold')

    # Add value labels on top of bars
    for i in range(len(x)):
        plt.text(x[i] - width, df_attempts['3PT Attempts'][i], 
                 f'{df_attempts["3PT Attempts"][i]:.1f}', 
                 ha='center', va='bottom')
        plt.text(x[i], df_attempts['2PT Attempts'][i], 
                 f'{df_attempts["2PT Attempts"][i]:.1f}', 
                 ha='center', va='bottom')
        plt.text(x[i] + width, df_attempts['FT Attempts'][i], 
                 f'{df_attempts["FT Attempts"][i]:.1f}', 
                 ha='center', va='bottom')

    plt.legend(title='Shot Type', title_fontsize=12, fontsize=10,
              frameon=True, edgecolor='black',
              facecolor='white', framealpha=0.9)
    plt.grid(True, axis='y', alpha=0.2, linestyle='--')
    plt.tight_layout()
    return plt.gcf()

def create_pace_scoring_plot(combined_df):
    """Create scatter plot of pace vs scoring with correlation analysis."""
    plt.figure(figsize=(10, 7))
    colors = {
        '2003/04': '#FF0000',
        '2013/14': '#4B0082',
        '2023/24': '#1E90FF'
    }
    markers = {
        '2003/04': 'o',
        '2013/14': 's',
        '2023/24': '^'
    }

    for season in ['2003/04', '2013/14', '2023/24']:
        season_data = combined_df[combined_df['Season'] == season]
        plt.scatter(season_data['Pace'], 
                   season_data['PTS'], 
                   c=colors[season], 
                   marker=markers[season],
                   s=120,
                   alpha=0.7,
                   label=season)
        
        z = np.polyfit(season_data['Pace'], season_data['PTS'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(season_data['Pace'].min(), season_data['Pace'].max(), 100)
        plt.plot(x_trend, p(x_trend), '--', color=colors[season], alpha=0.7)

    # Add correlation coefficients
    for i, season in enumerate(['2003/04', '2013/14', '2023/24']):
        season_data = combined_df[combined_df['Season'] == season]
        corr = season_data['Pace'].corr(season_data['PTS']).round(3)
        plt.text(0.02, 0.98 - i*0.05,
                f'{season} correlation: {corr}',
                transform=plt.gca().transAxes,
                color=colors[season],
                fontweight='bold',
                fontsize=9)

    # Add season averages
    avg_text = ""
    for season in ['2003/04', '2013/14', '2023/24']:
        season_data = combined_df[combined_df['Season'] == season]
        avg_pace = season_data['Pace'].mean()
        avg_text += f"{season} Avg Pace: {avg_pace:.1f}\n"

    plt.text(0.98, 0.02, avg_text,
             transform=plt.gca().transAxes,
             color='black',
             fontweight='bold',
             fontsize=8,
             ha='right',
             va='bottom',
             bbox=dict(facecolor='white', 
                      edgecolor='black', 
                      alpha=0.7))

    plt.title('Relationship between Pace and Scoring (2003-2024)', 
              fontsize=14, pad=20, fontweight='bold')
    plt.xlabel('Pace (Possessions per 48 minutes)', fontsize=11, fontweight='bold')
    plt.ylabel('Points Per Game', fontsize=11, fontweight='bold')
    plt.grid(True, alpha=0.2, linestyle='--')
    
    plt.legend(title='Season', title_fontsize=10, fontsize=9,
              frameon=True, edgecolor='black',
              facecolor='white', framealpha=0.9,
              markerscale=1.2,
              bbox_to_anchor=(0.01, 0.68),
              loc='lower left')
    plt.tight_layout()
    return plt.gcf()

def main():
    # Set the style
    sns.set_theme(style="whitegrid")
    
    # Load and prepare data
    nba_03, nba_13, nba_23, combined_df = load_and_prepare_data(
        'NBA_03.csv', 'NBA_13.csv', 'NBA_23.csv'
    )
    
    # Calculate averages and changes.
    df_attempts = calculate_shot_averages(nba_03, nba_13, nba_23)
    shot_changes = calculate_shot_percentage_changes(df_attempts)
    
    # Create all plots.
    create_scoring_attempts_plot(combined_df)
    plt.savefig('Figures/Scoring.png', format='png', dpi=300)
    create_shot_attempts_comparison(df_attempts)
    plt.savefig('Figures/Evolution.png', format='png', dpi=300)
    create_pace_scoring_plot(combined_df)
    plt.savefig('Figures/Pace.png', format='png', dpi=300)
    
    # Print statistics
    print("\nPercentage Changes in Shot Attempts (2003/04 to 2023/24):")
    print("-" * 60)
    for shot_type, change in shot_changes.items():
        print(f"{shot_type}: {change:+.1f}%")
        
    print("\nAverage Attempts per Game by Season:")
    print("-" * 40)
    print(df_attempts.round(1))
    
    # Show all plots
    plt.show()


if __name__ == "__main__":
    main()