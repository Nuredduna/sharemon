from sharemon import ShareMon, Share, ShareValue, Alarm, isLower, isHigher, readShares

import unittest

class TestShareMon(unittest.TestCase):

    def test_simple_use_cases(self):

        share_apple = Share("AAPL", "Apple, Inc")
        share_ibm = Share("IBM", "IBM Corp")
        share_tesla = Share("TSLA", "Tesla")
        share_siemens = Share("DE0007236101", "Siemens")
        share_google = Share("GOOG", "Alphabet")
        share_xxx = Share("XXX", "Unknown")

        share_apple.limit = [25,10]
        share_siemens.limit = [20,50]
        self.assertEqual([25,10], share_apple.limit)

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

        # Apple and Siemens share values below threshold, two alarms triggered.
        alarms = sm.update([ShareValue(share_siemens, 125), ShareValue(share_xxx, 15), ShareValue(share_apple, 90), ShareValue(share_google, 30)])
        self.assertEqual(2, len(alarms))
        self.assertEqual("decreased", alarms[0].type_of_alarm)
        self.assertEqual("increased", alarms[1].type_of_alarm)

    def test_limit_checks(self):

        self.assertTrue(isLower(80, 30, 30))
        self.assertTrue(isLower(80, 30, 0))
        self.assertFalse(isLower(100, 80, 100))

        self.assertTrue(isHigher(100, 125, 20))
        self.assertFalse(isHigher(100, 300, 0))

    def test_readShares(self):

        shares_local = readShares("local")
        self.assertEqual(3, len(shares_local))

        shares_file = readShares("file")
        self.assertEqual(3, len(shares_file))

        share_apple = shares_local[0]
        share_ibm = shares_local[1]
        share_tesla = shares_local[2]

        share_siemens = shares_file[0]
        share_google = shares_file[1]
        share_xxx = shares_file[2]

        self.assertEqual("AAPL", share_apple.share_id)
        self.assertEqual("IBM", share_ibm.share_id)
        self.assertEqual("TSLA", share_tesla.share_id)
        self.assertEqual("DE0007236101", share_siemens.share_id)
        self.assertEqual("GOOG", share_google.share_id)
        self.assertEqual("XXX", share_xxx.share_id)

    def share_present_in_alarms(self, share, alarms):
        for alarm in alarms:
            if alarm.monitored_share_value.share == share:
                return True
        return False
