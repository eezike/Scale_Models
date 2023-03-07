import unittest
from machine import Machine
import os
import shutil
import threading
import time

class TestMachine(unittest.TestCase):
    # Note, need to initialize machines in each function
    # due to thread memory leaks and unittest specs.

    def testInitialization(self) -> None:
        # Init the machines for the test
        self.machine1 = Machine(1, True)
        self.machine2 = Machine(2, True)
        self.machine3 = Machine(3, True)

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
        self.assertEqual(machine_clock.clock.clock_rate, 7)
        machine_clock.close()

        # Check machine_id init failure
        with self.assertRaises(SystemExit) as cm:
            machine_fail = Machine(4, True)
            self.assertEqual(cm.exception.args[0], 1)
            machine_fail.close()

        # Test log creation
        test_dir = "test_dir"
        machine_log = Machine(1, True, None, test_dir)
        log_file_path = f"{test_dir}/machine{1}.log"
        self.assertTrue(os.path.exists(log_file_path))
        machine_log.close()

        # Test log deletion
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        self.assertFalse(os.path.exists(log_file_path))

        # Close the machines for the test
        self.machine1.close()
        self.machine2.close()
        self.machine3.close()

        print("testInitialization passed")

    def testConnection(self) -> None:
        # Init machines
        self.machine1 = Machine(1, True)
        self.machine2 = Machine(2, True)
        self.machine3 = Machine(3, True)

        # Set connection wait time for speedy testing purposes
        self.machine1.CONNECTION_WAIT = 0
        self.machine2.CONNECTION_WAIT = 0
        self.machine3.CONNECTION_WAIT = 0

        # Ensure machines are not connected at first
        self.assertFalse(self.machine1.connected)
        self.assertFalse(self.machine2.connected)
        self.assertFalse(self.machine3.connected)

        # Connect function for thread purposes
        def connect(machine):
            machine.init_connection()

        # Connect all the machines (wait 1 secs to ensure they have connected)
        threading.Thread(target = connect, args = (self.machine1,)).start()
        threading.Thread(target = connect, args = (self.machine2,)).start()
        threading.Thread(target = connect, args = (self.machine3,)).start()
        time.sleep(1)

        # Ensure machines have connected
        self.assertTrue(self.machine1.connected)
        self.assertTrue(self.machine2.connected)
        self.assertTrue(self.machine3.connected)

        # Close the machines for the test
        self.machine1.close()
        self.machine2.close()
        self.machine3.close()

        print("testConnection passed")

    def testCommunications(self) -> None:
        pass

    def testLogs(self) -> None:

        # Test log creation
        test_dir = "test_dir"
        machine_log = Machine(1, True, None, test_dir)
        log_file_path = f"{test_dir}/machine{1}.log"
        self.assertTrue(os.path.exists(log_file_path))
        
        # Open the log file
        with open(log_file_path, "r") as log_file:
            log_contents = log_file.read()

        # Test all log events
        machine_log.log_event("initial")
        machine_log.log_event("receive")
        machine_log.log_event("send")
        machine_log.log_event("internal")

        with open(log_file_path, "r") as log_file:
            log_contents = log_file.read()

        expected_log_entries = [
            "[Machine initialized with clock_rate:",
            "[receive_event,",
            "[send_event,",
            "[internal_event,",
        ]

        for log_entry in expected_log_entries:
            self.assertIn(log_entry, log_contents)

        # Test log deletion
        machine_log.close()
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
        self.assertFalse(os.path.exists(log_file_path))

        print("testLogs passed")

class TestLogicalClocks(unittest.TestCase):
    def testTick(self):
        pass

    def testUpdate(self):
        pass

if __name__ == '__main__':
    print("Begining unit tests...")
    unittest.main()