import unittest
import pandas as pd
from slice_barcode import slice_barcode
class TestSliceBarcode(unittest.TestCase):
    ''''''

    def test_slice_barcode(self):
        # Create a sample DataFrame with a barcode column
        df = pd.DataFrame({'barcode': ['1234567890', '0987654321', '5555555555']})

        # Call the slice_barcode function to create a new column with the first 5 characters of the barcode
        df = slice_barcode(df, 'barcode_prefix', 'barcode', 0, 5)

        # Verify that the new column has been added with the correct sliced values
        self.assertEqual(list(df.columns), ['barcode_prefix', 'barcode'])
        self.assertEqual(list(df['barcode_prefix']), ['12345', '09876', '55555'])

if __name__ == '__main__':
    unittest.main()
