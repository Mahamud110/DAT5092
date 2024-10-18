
import unittest
import matplotlib.pyplot as plt
import os
import numpy as np


class TestFileExists(unittest.TestCase):
    # Create Unittest class to see if csv file exists

    def test_file_exists(self):
        # specifies the file path of file you wanna check
        file_path = r'C:\Unit_Testing\DAT5092\DAT5092\linear_data.csv'

        self.assertTrue(os.path.isfile(file_path), f"{file_path} does not exist.")


if __name__ == '__main__':
            unittest.main()


df = np.loadtxt(r'C:\Unit_Testing\DAT5092\DAT5092\linear_data.csv',delimiter=',',skiprows=1)

x = df[:,0]
y = df[:,1]

plt.plot(x,y)
plt.show()
