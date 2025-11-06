# %%
import mne
import numpy as np
import pyxdf
import matplotlib.pyplot as plt
from mne.viz import plot_topomap
plt.rcParams['animation.ffmpeg_path'] = 'C:\\ffmpeg\\bin\\ffmpeg.exe'

# XDF 파일 읽기
file_path = 'eeg.xdf'
streams, header = pyxdf.load_xdf(file_path)

# 각 트리거 별로 딕셔너리 생성
event_id_dict = {
  '': -3,
  'start': -1,
  'end': -2,
  'rest': 0
}

# 데이터 스트림 선택 
for stream in streams:
    if stream['info']['type'][0] == 'EEG':  # EEG 데이터 선택
        eeg_data = np.array(stream['time_series']).T
        eeg_times = np.array(stream['time_stamps'])
        if not eeg_times.size:
            eeg_times = np.arange(eeg_data.shape[1]) / float(stream['info']['nominal_srate'][0])
        # 채널 이름 추출
        ch_names = [ch['label'][0] for ch in stream['info']['desc'][0]['channels'][0]['channel']]
    elif stream['info']['name'][0] == 'P002_S003': # Trigger 선택
        event_ids = np.array(stream['time_series'])
        event_times = np.array(stream['time_stamps'])

# 모든 채널을 EEG 타입으로 설정
ch_types = ['eeg'] * len(ch_names) 

# 샘플링 빈도는 데이터에 맞게 설정
sfreq = 100

# MNE 정보 객체 생성
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

# MNE RawArray 객체 생성
raw = mne.io.RawArray(eeg_data, info)

# 이벤트 정보 추출
unique_events = np.unique(event_ids)
mapped_event_ids = np.vectorize(event_id_dict.get)(event_ids,-1)

# Trigger 정보
event_samples = (event_times - eeg_times[0]) * sfreq
events = np.column_stack([event_samples.astype(int), np.zeros(len(event_samples), dtype=int), mapped_event_ids])

# 몽타주 설정
montage = mne.channels.make_standard_montage('standard_1020')
raw.set_montage(montage)

epochs = mne.Epochs(raw, events, event_id={'start': -1, 'end': -2},
                    tmin=-0.2, tmax=0.5, baseline=None, preload=True)

evoked = epochs.average()

# 가운데 시간점에서의 topomap 시각화
mid_index = evoked.data.shape[1] // 2  # 데이터의 중간 인덱스
fig, ax = plt.subplots()
plot_topomap(evoked.data[:, mid_index], evoked.info, axes=ax, show=True)

# 시간 배열 설정
times = np.linspace(evoked.times[0], evoked.times[-1], len(evoked.times))

# 애니메이션 생성
fig, anim = evoked.animate_topomap(
    times=times, 
    ch_type='eeg', 
    frame_rate=10,   # 초당 프레임 수
    blit=False       # blitting을 사용하지 않음 (호환성 문제 방지)
)

# 애니메이션 저장
anim.save('topomap_animation.mp4', writer='ffmpeg', fps=10)
print('done')