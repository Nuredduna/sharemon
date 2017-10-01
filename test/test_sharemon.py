from sharemon import ShareMon, Share, ShareValue, Alarm

import unittest

class TestShareMon(unittest.TestCase):

    def test_simple_use_cases(self):

        share_apple = Share("AAPL", "Apple, Inc")
        share_ibm = Share("IBM", "IBM Corp")
        share_tesla = Share("TSLA", "Tesla")
        share_siemens = Share("DE0007236101", "Siemens")
        share_google = Share("GOOG", "Alphabet")
        share_xxx = Share("XXX", "Unknown")

        monitored_shares = [ShareValue(share_apple, 100), ShareValue(share_ibm, 40), ShareValue(share_siemens, 80)]
        sm = ShareMon(monitored_shares)

        # Apple share value increases, no alarm triggered.
        alarms = sm.update([ShareValue(share_xxx, 10), ShareValue(share_apple, 120), ShareValue(share_google, 30)])
        self.assertEqual(0, len(alarms))

        # Apple share value below threshold, one alarm triggered.
        alarms = sm.update([ShareValue(share_xxx, 15), ShareValue(share_apple, 90), ShareValue(share_google, 30)])
        self.assertEqual(1, len(alarms))
        self.assertEqual(share_apple, alarms[0].monitored_share_value.share)
        self.assertEqual(90, alarms[0].value)

        # Apple and Siemens share values below threshold, two alarms triggered.
        alarms = sm.update([ShareValue(share_siemens, 30), ShareValue(share_xxx, 15), ShareValue(share_apple, 90), ShareValue(share_google, 30)])
        self.assertEqual(2, len(alarms))
        self.assertTrue(self.share_present_in_alarms(share_apple, alarms))
        self.assertTrue(self.share_present_in_alarms(share_siemens, alarms))
        self.assertFalse(self.share_present_in_alarms(share_xxx, alarms))

    def share_present_in_alarms(self, share, alarms):
        for alarm in alarms:
            if alarm.monitored_share_value.share == share:
                return True
        return False
