import unittest
import pandas as pd
from parameterized import parameterized
from fill_non_blank_down import fill_non_blank_down, fill_non_blank_down2

class TestFillNonBlankDown(unittest.TestCase):

    @parameterized.expand([
        (pd.DataFrame({'A': [1, 2, 3, pd.NA, 5]}), 'A', [1, 2, 3, 5, 5]),
        (pd.DataFrame({'A': [pd.NA, 2, pd.NA, 4, pd.NA]}), 'A', [2, 2, 4, 4, 4]),
        (pd.DataFrame({'A': [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]}), 'A', [pd.NA, pd.NA, pd.NA, pd.NA, pd.NA]),
        (pd.DataFrame({'A': [1, 2, 3, 4, 5]}), 'A', [1, 2, 3, 4, 5])
    ])
    def test_fill_non_blank_down(self, df, column, expected):
        # Call the fill_non_blank_down function to fill NaN values in the specified column
        df = fill_non_blank_down(df, column)

        # Verify that the NaN values have been filled down correctly
        self.assertEqual(list(df[column]), expected)

    @parameterized.expand([
        (pd.DataFrame({'A': [1, 2, pd.NA, 4, 5]}), 'A', [1, 2, 2, 4, 5]),
        (pd.DataFrame({'A': [1, pd.NA, 3, pd.NA, 5]}), 'A', [1, 1, 3, 3, 5]),
        (pd.DataFrame({'A': [7, pd.NA, pd.NA, pd.NA, 5]}), 'A', [7, 7, 7, 7, 5]),
        (pd.DataFrame({'A': [1, 2, 3, 4, 5]}), 'A', [1, 2, 3, 4, 5])
    ])
    def test_fill_non_blank_down2(self, df, column, expected):
        # Call the fill_non_blank_down2 function to fill NaN values in the specified column
        df = fill_non_blank_down2(df, column)

        # Verify that the NaN values have been filled down correctly
        self.assertEqual(list(df[column]), expected)

if __name__ == '__main__':
    unittest.main()