import unittest

class TestMachine(unittest.TestCase):
    def testInitialization():
        # test when you input a wrong process id (can either be 1, 2, or 3)
        # test when you input the right process id for the machine
        # test connection here as well
        pass

    def testCommunications():
        # going to be the meat of the unit testing...
        # how can we break up receive and send threads
        pass

    def testLogs():
        # test different log events with a sample log file
        pass

class TestLogicalClocks(unittest.TestCase):
    def testTick():
        pass

    def testUpdate():
        pass

if __name__ == '__main__':
    unittest.main()