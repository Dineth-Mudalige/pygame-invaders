from scipy.signal import butter,lfilter

class Filter:
    def __init__(self,input_matrix):
        self.input_matrix = input_matrix

    def butter_bandpass(self, lowcut, highcut, sampling_rate, order):
        nyquist = 0.5 * sampling_rate
        low = lowcut / nyquist
        high = highcut / nyquist
        b,a = butter(order, [low, high], btype='band')
        y = lfilter(b,a,self.input_matrix)
        return y