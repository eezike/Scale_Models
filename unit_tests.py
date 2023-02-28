import unittest

class TestMachine(unittest.TestCase):
    def testInitialization():
        # test when you input a wrong process id (can either be 1, 2, or 3)
        # test when you input the right process id for the machine
        # maybe test the configuration class here
        pass

class TestLogicalClocks(unittest.TestCase):
    pass

if __name__ == '__main__':
    unittest.main()