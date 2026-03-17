# %%
import mne
import numpy as np
import pyxdf
import matplotlib
matplotlib.use('qtagg')  # 혹은 사용 가능한 다른 GUI 백엔드를 사용

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
    elif stream['info']['name'][0] == 'P001_S003': # Trigger 선택
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

# 채널 선택
picks = mne.pick_types(raw.info, eeg=True)

# 이벤트 시간 인덱스 찾기
start_idx = np.where(mapped_event_ids == event_id_dict['start'])
end_idx = np.where(mapped_event_ids == event_id_dict['end'])
print(start_idx)

if len(start_idx) > 0 and len(end_idx) > 0 and start_idx[0] < end_idx[0]:
    start_time = event_samples[start_idx[0]]
    end_time = event_samples[end_idx[0]]

    # 데이터 슬라이싱
    start_sample = int(start_time)
    end_sample = int(end_time)
    sliced_raw = raw.copy().crop(tmin=raw.times[start_sample], tmax=raw.times[end_sample])

    # 플롯 생성
    sliced_raw.plot(events=events, event_id=event_id_dict, color='b', scalings='auto', picks=picks, block=True, n_channels=len(ch_names))