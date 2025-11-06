from pylsl import StreamInlet, resolve_stream
import numpy as np
import matplotlib.pyplot as plt
import mne
from mne.viz import plot_topomap
import time

# EEG 스트림을 찾습니다
eeg_streams = resolve_stream('type', 'EEG')

# 첫 번째 스트림으로 StreamInlet을 생성합니다
eeg_inlet = StreamInlet(eeg_streams[0])

# 스트림 정보를 가져옵니다
info = eeg_inlet.info() 

# StreamInfo 객체에서 채널 정보를 읽습니다
channels = info.desc().child("channels").child("channel")
channel_names = []

while not channels.empty():
    # 각 채널의 이름을 리스트에 추가합니다
    channel_names.append(channels.child_value("label"))
    channels = channels.next_sibling()

# 채널 타입을 모두 'eeg'로 설정
ch_types = ['eeg'] * len(channel_names)

# 샘플링 빈도 추출
sfreq = info.nominal_srate()

# 데이터 수집을 위한 변수 초기화
all_samples = []
start_time = time.time()

print("Collecting data for 5 seconds...")
# 5초 동안 데이터 수집
while time.time() - start_time < 5:
    sample, timestamp = eeg_inlet.pull_sample()
    if sample:
        all_samples.append(sample)
print("Data collected.")

# 데이터를 numpy 배열로 변환
data_array = np.array(all_samples).T  # Transpose to match MNE structure

# MNE 정보 객체 생성
info = mne.create_info(ch_names=channel_names, sfreq=sfreq, ch_types=ch_types)

# MNE RawArray 객체 생성
raw = mne.io.RawArray(data_array, info)

# 몽타주 설정 (10-20 시스템)
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

# 데이터 평균 처리
data, times = raw[:]
average_data = np.mean(data, axis=1)

# 토포그래픽 맵 시각화
fig, ax = plt.subplots()
plot_topomap(average_data, raw.info, axes=ax, show=True)