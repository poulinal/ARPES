import unittest
import numpy as np
from commonWidgets import rescale

class TestStringMethods(unittest.TestCase):
    def testRescale(self):
        a = np.arange(1, 11)
        self.assertEqual(np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]), a.rescale(a, 0, 1))

if __name__ == '__main__':
    unittest.main()