import unittest
from package.OrbitExtractor import targetOrbit


class tester(unittest.TestCase):
    runs = targetOrbit.get_runs()
    