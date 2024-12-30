import unittest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from Project import (
    load_and_prepare_data,
    calculate_shot_averages,
    calculate_shot_percentage_changes,
    create_scoring_attempts_plot,
    create_shot_attempts_comparison,
    create_pace_scoring_plot
)

class TestNBAAnalysis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create sample data for testing."""
        # Create sample DataFrames that mimic the structure of the NBA data
        cls.sample_data_03 = pd.DataFrame({
            'Team': ['TeamA', 'TeamB', 'TeamC'],
            '3PA': [15.0, 16.0, 17.0],
            '2PA': [55.0, 54.0, 53.0],
            'FTA': [25.0, 24.0, 23.0],
            'PTS': [95.0, 98.0, 97.0],
            'Pace': [90.0, 91.0, 92.0]
        })
        
        cls.sample_data_13 = pd.DataFrame({
            'Team': ['TeamA', 'TeamB', 'TeamC'],
            '3PA': [20.0, 21.0, 22.0],
            '2PA': [50.0, 49.0, 48.0],
            'FTA': [22.0, 21.0, 20.0],
            'PTS': [100.0, 102.0, 101.0],
            'Pace': [92.0, 93.0, 94.0]
        })
        
        cls.sample_data_23 = pd.DataFrame({
            'Team': ['TeamA', 'TeamB', 'TeamC'],
            '3PA': [35.0, 36.0, 37.0],
            '2PA': [45.0, 44.0, 43.0],
            'FTA': [20.0, 19.0, 18.0],
            'PTS': [115.0, 118.0, 117.0],
            'Pace': [98.0, 99.0, 100.0]
        })
        
        # Save temporary CSV files for testing
        cls.sample_data_03.to_csv('test_03.csv', index=False)
        cls.sample_data_13.to_csv('test_13.csv', index=False)
        cls.sample_data_23.to_csv('test_23.csv', index=False)

    def test_load_and_prepare_data(self):
        """Test data loading and preparation."""
        nba_03, nba_13, nba_23, combined_df = load_and_prepare_data(
            'test_03.csv', 'test_13.csv', 'test_23.csv'
        )
        
        # Test data loading
        self.assertEqual(len(nba_03), 3)
        self.assertEqual(len(nba_13), 3)
        self.assertEqual(len(nba_23), 3)
        self.assertEqual(len(combined_df), 9)
        
        # Test year columns
        self.assertTrue('Year' in nba_03.columns)
        self.assertTrue('Season' in nba_03.columns)
        self.assertEqual(nba_03['Year'].unique()[0], '2003/04')
        self.assertEqual(nba_13['Year'].unique()[0], '2013/14')
        self.assertEqual(nba_23['Year'].unique()[0], '2023/24')

    def test_calculate_shot_averages(self):
        """Test shot averages calculation."""
        averages_df = calculate_shot_averages(
            self.sample_data_03, 
            self.sample_data_13, 
            self.sample_data_23
        )
        
        # Test DataFrame structure
        self.assertEqual(len(averages_df), 3)
        self.assertEqual(list(averages_df.columns), 
                        ['3PT Attempts', '2PT Attempts', 'FT Attempts'])
        
        # Test average calculations
        np.testing.assert_almost_equal(
            averages_df.loc['2003/04', '3PA'].mean(), 
            self.sample_data_03['3PA'].mean()
        )
        np.testing.assert_almost_equal(
            averages_df.loc['2023/24', '2PA'].mean(), 
            self.sample_data_23['2PA'].mean()
        )

    def test_calculate_shot_percentage_changes(self):
        """Test percentage changes calculation."""
        averages_df = calculate_shot_averages(
            self.sample_data_03, 
            self.sample_data_13, 
            self.sample_data_23
        )
        changes = calculate_shot_percentage_changes(averages_df)
        
        # Test structure
        self.assertEqual(len(changes), 3)
        self.assertTrue(all(key in changes for key in 
                          ['3PT Attempts', '2PT Attempts', 'FT Attempts']))
        
        # Test percentage calculations
        expected_3pt_change = ((36.0 - 16.0) / 16.0) * 100  # Example calculation
        self.assertAlmostEqual(
            changes['3PT Attempts'],
            expected_3pt_change,
            places=1
        )

    def test_plot_creation(self):
        """Test that plots are created without errors."""
        combined_df = pd.concat([
            self.sample_data_03.assign(Year='2003/04', Season='2003/04'),
            self.sample_data_13.assign(Year='2013/14', Season='2013/14'),
            self.sample_data_23.assign(Year='2023/24', Season='2023/24')
        ])
        
        averages_df = calculate_shot_averages(
            self.sample_data_03, 
            self.sample_data_13, 
            self.sample_data_23
        )

        # Test each plot creation
        try:
            fig1 = create_scoring_attempts_plot(combined_df)
            self.assertIsInstance(fig1, plt.Figure)
            plt.close(fig1)

            fig2 = create_shot_attempts_comparison(averages_df)
            self.assertIsInstance(fig2, plt.Figure)
            plt.close(fig2)

            fig3 = create_pace_scoring_plot(combined_df)
            self.assertIsInstance(fig3, plt.Figure)
            plt.close(fig3)
        except Exception as e:
            self.fail(f"Plot creation failed with error: {str(e)}")

    def test_data_integrity(self):
        """Test data integrity and relationships."""
        nba_03, nba_13, nba_23, combined_df = load_and_prepare_data(
            'test_03.csv', 'test_13.csv', 'test_23.csv'
        )
        
        # Test that PTS increases with time (as per sample data)
        avg_pts_03 = nba_03['PTS'].mean()
        avg_pts_13 = nba_13['PTS'].mean()
        avg_pts_23 = nba_23['PTS'].mean()
        
        self.assertLess(avg_pts_03, avg_pts_13)
        self.assertLess(avg_pts_13, avg_pts_23)
        
        # Test that 3PA increases while 2PA decreases
        self.assertLess(nba_03['3PA'].mean(), nba_23['3PA'].mean())
        self.assertGreater(nba_03['2PA'].mean(), nba_23['2PA'].mean())

    @classmethod
    def tearDownClass(cls):
        """Clean up temporary files."""
        import os
        for file in ['test_03.csv', 'test_13.csv', 'test_23.csv']:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main(verbosity=2)