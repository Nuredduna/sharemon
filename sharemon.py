#!/usr/bin/env python3

local_shares = (("AAPL", "Apple, Inc"), ("IBM", "IBM Corp"), ("TSLA", "Tesla"))

def deviation(base_value, percentage_value):

    """ Calculates the difference in percentage of two given values. """
    percentage = percentage_value * 100 / base_value

    return 100 - percentage if percentage <= 100 else percentage - 100


def isLower(mon_share_value, realtime_share_value, limit):

    """ Checks if the limit is exceeded (below specified threshold). """
    deviation_val = deviation(mon_share_value, realtime_share_value)

    return False if deviation_val < limit else True


def isHigher(mon_share_value, realtime_share_value, limit):

    """ Checks if the limit is exceeded (above specified threshold). """
    deviation_val = deviation(mon_share_value, realtime_share_value)

    return True if (limit != 0 and deviation_val > limit) else False

def readSharesFromLocal():
    """ Reads the share id and the comment from local_shares.
        Returns a list of Share objects.
    """
    shares_read = []

    for share in local_shares:
        shares_read.append(Share(share[0], share[1]))

    return shares_read

def readSharesFromFile():
    """ Reads the share id and the comment from a file.
        Returns a list of Share objects.
    """
    shares_read = []

    fobj = open("test/shares.txt", "r")

    for line in fobj:
        line = line.strip()
        share = line.split("|")
        shares_read.append(Share(share[0], share[1]))

    fobj.close()

    return shares_read

def readShares(source):
    """ Reads shares from a specified source.
        Returns a list of Share objects.
        For now local and text file is supported
    """
    if source == "local":
        return readSharesFromLocal()
    else:
        return readSharesFromFile()


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
                    if mon_val.value <= val.value:
                        if isHigher(mon_val.value, val.value, val.share.getUpperLimit()):
                            alarms.append(Alarm(mon_val, val.value, "increased"))
                    elif isLower(mon_val.value, val.value, val.share.getLowerLimit()):
                        alarms.append(Alarm(mon_val, val.value, "decreased"))

        return alarms

class Share:
    """ Represents a single share. """

    def __init__(self, share_id, comment="", limit=[0,100]):
        self.share_id = share_id
        self.comment = comment
        self._limit = limit

    def setLimit(self, limit):
        """ Sets the limit for the specified share, increasing, decreasing, values in percent """
        self._limit = limit

    def getLimit(self):
        """ Gets the specified limit for a share, increasing, decreasing, values in percent """
        return self._limit

    def getLowerLimit(self):
        return self._limit[1]

    def getUpperLimit(self):
        return self._limit[0]

    limit = property(getLimit, setLimit)

class ShareValue:
    """ Represents a value for a share (eg. a share price). """

    def __init__(self, share, value):
        self.share = share
        self.value = value


class Alarm:
    """ Represents an alarm that was triggered for a particular share. """

    def __init__(self, monitored_share_value, current_value, type_of_alarm):
        self.monitored_share_value = monitored_share_value
        self.value = current_value
        self.type_of_alarm = type_of_alarm

