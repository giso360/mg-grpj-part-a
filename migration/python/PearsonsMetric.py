import numpy as np
import math as m


class PearsonsMetric:

    def __init__(self, X, Y):
        """
        Class constructor.
        @param X: First vector
        @param Y: Second vector
        """
        self.X = X
        self.Y = Y

    def get_pearson(self):
        """"
        Returns a similarity metric of two vectors based on Pearson's correlation
        calculated from the following element-wise operation:
        r = SUM((x-x_bar)*(y-y_bar)) / sqrt(SUM((x-x_bar)**2)*SUM((y-y_bar)**2))
        where x_bar, y_bar are the means of each vector.
        @param X: The first vector.
        @param Y: The second vector.
        @return The similarity metric as a scalar value.
        """
        if np.all(self.X == 0) and np.all(self.Y == 0):
            return 1
        x_bar = np.mean(self.X)
        y_bar = np.mean(self.Y)
        x_minus_bar = self.X - x_bar
        x_minus_bar_squared = np.square(x_minus_bar)
        y_minus_bar = self.Y - y_bar
        y_minus_bar_squared = np.square(y_minus_bar)
        numeratori = np.multiply(x_minus_bar, y_minus_bar)
        numerator = np.sum(numeratori)
        denominator = m.sqrt(np.sum(x_minus_bar_squared) * np.sum(y_minus_bar_squared))
        if denominator == 0:
            return 0
        else:
            return numerator / denominator
