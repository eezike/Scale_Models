import unittest
from machine import Machine
import os
import shutil

class TestMachine(unittest.TestCase):
    def setUp(self) -> None:
        self.machine1 = Machine(1, True)
        self.machine2 = Machine(2, True)
        self.machine3 = Machine(3, True)

    def testInitialization(self) -> None:
        
        # Check machine initialization
        self.assertEqual(self.machine1.MACHINE_ID, 1)
        self.assertEqual(self.machine1.PORT, 50050)
        self.assertEqual(self.machine1.PEER_PORTS, [50051, 50052])

        self.assertEqual(self.machine2.MACHINE_ID,2)
        self.assertEqual(self.machine2.PORT, 50051)
        self.assertEqual(self.machine2.PEER_PORTS, [50050, 50052])

        self.assertEqual(self.machine3.MACHINE_ID, 3)
        self.assertEqual(self.machine3.PORT, 50052)
        self.assertEqual(self.machine3.PEER_PORTS, [50050, 50051])

        # Check pre-determined clock initialization
        machine_clock = Machine(1, True, 7)
        self.assertEqual(machine_clock.clock_rate, 7)

        # Check machine_id init failure
        with self.assertRaises(SystemExit) as cm:
            machine_fail = Machine(4, True)
            self.assertEqual(cm.exception.args[0], 1)
            del machine_fail

        # Test log creation
        test_dir = "test_dir"
        machine_log = Machine(1, True, None, test_dir)
        log_file_path = f"{test_dir}/machine{1}.log"
        self.assertTrue(os.path.exists(log_file_path))
        machine_log.log_file.close()
        del machine_log

        # Test log deletion
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        self.assertFalse(os.path.exists(log_file_path))

    def testCommunications(self) -> None:
        # going to be the meat of the unit testing...
        # how can we break up receive and send threads
        pass

    def testLogs(self) -> None:
        # test different log events with a sample log file
        pass

class TestLogicalClocks(unittest.TestCase):
    def testTick(self):
        pass

    def testUpdate(self):
        pass

if __name__ == '__main__':
    unittest.main()