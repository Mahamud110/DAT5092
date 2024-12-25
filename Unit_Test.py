import unittest
import pandas as pd
import numpy as np

class TestNBAAnalysis(unittest.TestCase):

    def setUp(self):
        # Load data from CSV files
        self.nba_03 = pd.read_csv('NBA_03.csv')
        self.nba_13 = pd.read_csv('nba_13.csv')
        self.nba_23 = pd.read_csv('NBA_23.csv')

    def test_combined_dataframe(self):
        """Test combining dataframes and adding a year column."""
        self.nba_03['Year'] = '2003/04'
        self.nba_13['Year'] = '2013/14'
        self.nba_23['Year'] = '2023/24'
        combined_df = pd.concat([self.nba_03, self.nba_13, self.nba_23])

        # Check number of rows
        expected_row_count = len(self.nba_03) + len(self.nba_13) + len(self.nba_23)
        self.assertEqual(combined_df.shape[0], expected_row_count)

        # Check required columns exist
        for column in ['PTS', '3PA', 'Year']:
            self.assertIn(column, combined_df.columns)

    def test_trendline_calculation(self):
        """Test trendline (linear regression) calculations."""
        for df in [self.nba_03, self.nba_13, self.nba_23]:
            z = np.polyfit(df['3PA'], df['PTS'], 1)
            p = np.poly1d(z)
            x_vals = df['3PA']
            y_vals = p(x_vals)

            # Check that the trendline values have the expected shape
            self.assertEqual(len(y_vals), len(df['PTS']))

    def test_correlation_calculation(self):
        """Test correlation calculations between 3PA and PTS."""
        for df in [self.nba_03, self.nba_13, self.nba_23]:
            corr = df['3PA'].corr(df['PTS'])
            self.assertIsInstance(corr, float)
            self.assertGreaterEqual(corr, 0)  # Expect non-negative correlation

if __name__ == '__main__':
    unittest.main()
