#!/usr/bin/env python3


class ShareMon:
    """ Checks if values of monitored shares fall below a specified limit. """

    def __init__(self, monitored_share_values):
        """ Setup a Share Monitor with a given list of shares to monitor.
            monitored_shares_values: A list of 'ShareValue's where the values represents the alarm limits.
        """
        self.monitored_share_values = monitored_share_values

    def update(self, share_values):
        """ Check if monitored shares fall below specified limit.
            share_values: A list of shares with current values.
            Returns: a list of 'Alarm's
        """
        alarms = []

        for mon_val in self.monitored_share_values:
            for val in share_values:
                if mon_val.share.share_id == val.share.share_id:
                    if val.value < mon_val.value:
                        alarms.append(Alarm(mon_val, val.value))

        return alarms

class Share:
    """ Represents a single share. """

    def __init__(self, share_id, comment=""):
        self.share_id = share_id
        self.comment = comment


class ShareValue:
    """ Represents a value for a share (eg. a share price). """

    def __init__(self, share, value):
        self.share = share
        self.value = value


class Alarm:
    """ Represents an alarm that was triggered for a particular share. """

    def __init__(self, monitored_share_value, current_value):
        self.monitored_share_value = monitored_share_value
        self.value = current_value
