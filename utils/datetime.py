import time

from datetime import datetime


class Timer:
    """Measures the time between two events"""

    def __init__(self):
        """Create the object and start the virtual timer."""
        self._start = time.time()

    def get_duration(self) -> int:
        """Get number of seconds that passed from starting the virtual timer."""
        return int(time.time() - self._start)


def get_date_iso_8601(include_time=False):
    cutoff = 19 if include_time else 10
    return str(datetime.today())[:cutoff].replace(" ", "_").replace(":", "-")
