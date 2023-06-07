from ecgdetectors import Detectors
from matplotlib.axes import ma
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def R_correction(signal, peaks):

    num_peak=peaks.shape[0]
    peaks_corrected_list=list()
    for index in range(num_peak):
        i=peaks[index]
        cnt=i
        if cnt-1<0:
            break
        if signal[cnt]<signal[cnt-1]:
            while signal[cnt]<signal[cnt-1]:
                cnt-=1
                if cnt<0:
                    break
        elif signal[cnt]<signal[cnt+1]:
            while signal[cnt]<signal[cnt+1]:
                cnt+=1
                if cnt<0:
                    break
        peaks_corrected_list.append(cnt)
    peaks_corrected=np.asarray(peaks_corrected_list)            
    return peaks_corrected

def ex1(size, fs):

    heartbeat = pd.read_csv("./100.csv")
    detectors = Detectors(fs)
    r_peaks_pan = detectors.pan_tompkins_detector(heartbeat.iloc[:,2][0:size])
    r_peaks_pan= np.asarray(r_peaks_pan)
    corrected_R_peak=R_correction(heartbeat.iloc[:,2][0:size],r_peaks_pan)
    
    max_dist = 0
    idx = 0

    min_dist = 100000
    min_idx = []
    for x in range(len(corrected_R_peak)-1):
        if x == 0:
            continue

        dist = corrected_R_peak[x+1] - corrected_R_peak[x]
        print(f"Distance between {corrected_R_peak[x]} and {corrected_R_peak[x+1]} = {dist}")
        if dist > max_dist:
            max_dist = dist 
            idx = x
        elif min_dist > dist:
            min_dist = dist
            min_idx = [corrected_R_peak[x], corrected_R_peak[x+1]]
    
    print(f"Minimalna odległość (czerwona): {min_dist}")
    print(f"Maksymalna odległość (niebieska): {max_dist}")

    
    plt.plot(heartbeat.iloc[:,2][0:size])
    plt.plot(corrected_R_peak,heartbeat.iloc[:,2][0:size][corrected_R_peak], 'ro')
    plt.plot([corrected_R_peak[idx], corrected_R_peak[idx+1]], heartbeat.iloc[:,2][0:size][[corrected_R_peak[idx], corrected_R_peak[idx+1]]], 'bo', linestyle="--")
    plt.plot(min_idx, heartbeat.iloc[:,2][0:size][min_idx], 'red', linestyle="--")
    plt.show()
if __name__ == "__main__":
    size = 4000
    fs = 100
    ex1(size, fs)
