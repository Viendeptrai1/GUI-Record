class Interval:
    def __init__(self, xmin, xmax, text=""):
        self.xmin = xmin
        self.xmax = xmax
        self.text = text

class TextGrid:
    def __init__(self, xmin=0, xmax=0):
        self.xmin = xmin
        self.xmax = xmax
        self.intervals = [Interval(xmin, xmax, "")]

    def add_boundary(self, time):
        """
        Add a boundary at the specified time.
        Splits the interval containing 'time' into two.
        """
        if time <= self.xmin or time >= self.xmax:
            return

        # Find interval containing time
        for i, interval in enumerate(self.intervals):
            if interval.xmin < time < interval.xmax:
                # Split this interval
                new_interval_left = Interval(interval.xmin, time, interval.text)
                new_interval_right = Interval(time, interval.xmax, "") # New part is empty
                
                self.intervals[i] = new_interval_left
                self.intervals.insert(i + 1, new_interval_right)
                return

    def remove_boundary(self, time, tolerance=0.01):
        """
        Remove a boundary near the specified time.
        Merges the two adjacent intervals.
        """
        # Find boundary near time
        for i in range(len(self.intervals) - 1):
            boundary = self.intervals[i].xmax
            if abs(boundary - time) < tolerance:
                # Merge i and i+1
                left = self.intervals[i]
                right = self.intervals[i+1]
                
                merged = Interval(left.xmin, right.xmax, left.text + right.text)
                self.intervals[i] = merged
                del self.intervals[i+1]
                return

    def set_text(self, time, text):
        """
        Set text for the interval containing 'time'.
        """
        for interval in self.intervals:
            if interval.xmin <= time <= interval.xmax:
                interval.text = text
                return

    def get_interval(self, time):
        for interval in self.intervals:
            if interval.xmin <= time <= interval.xmax:
                return interval
        return None
