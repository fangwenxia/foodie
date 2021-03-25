# Script to show the time on the server

# Written by Scott D. Anderson
# scott.anderson@acm.org

import sys

from datetime import datetime

def now():
    """Returns a string for the current day and time.

    The output is in something close to Internet format. It's not really
    Internet format because it neither converts to UTC nor
    appends the time zone.  However, it will work nicely for MySQL.
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
    print(now())
