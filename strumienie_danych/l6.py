import wfdb

import neurokit2 as nk
import matplotlib.pyplot as plt

data = wfdb.rdrecord("JS00008", pn_dir="ecg-arrhythmia/WFDBRecords/01/010")

signals, fields = nk.ecg_process(data.p_signal[:,0], sampling_rate=data.fs)
print(fields)
nk.ecg_plot(signals, sampling_rate=data.fs)

record = wfdb.rdrecord('S0088_ST_V1', pn_dir='taichidb/1.0.2/Single-task/')

resp_signal = record.p_signal[:10000, 3]
plt.plot(resp_signal)

signals, info = nk.emg_process(resp_signal, sampling_rate=record.fs)

nk.emg_plot(signals, sampling_rate=record.fs)

plt.show()
