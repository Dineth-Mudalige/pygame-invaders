import numpy as np
import os

class DirectionClassifier:
    def __init__(self, tke_matrix, threshold):
        self.tke_matrix = tke_matrix
        self.threshold = threshold
    
    def create_commands(self):
        # column_1_squared = np.sum(self.tke_matrix[:,0])**2
        # column_2_squared = np.sum(self.tke_matrix[:,1])**2
        # squared_difference = column_1_squared - column_2_squared
        column1_max = np.max(self.tke_matrix[:,0])
        column2_max = np.max(self.tke_matrix[:,1])
        print("Channel 1 Max: ", column1_max)
        print("Channel 2 Max: ", column2_max)
        direction = "NONE"
        difference = column1_max - column2_max
        if difference > self.threshold:
            direction = "LEFT"
        elif difference < -1 * self.threshold:
            direction = "RIGHT"

        print("Derived direction: ", direction)

        return direction