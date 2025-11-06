# %%
import mne
import numpy as np
import pyxdf
import matplotlib
matplotlib.use('qtagg')  # 혹은 사용 가능한 다른 GUI 백엔드를 사용

# XDF 파일 읽기
file_path = 'eeg.xdf'
streams, header = pyxdf.load_xdf(file_path)

# %%
# 데이터 스트림 선택
for stream in streams:
    if stream['info']['type'][0] == 'EEG':  # EEG 데이터 선택
        eeg_data = np.array(stream['time_series']).T
        eeg_times = np.array(stream['time_stamps'])
        if not eeg_times.size:
            eeg_times = np.arange(eeg_data.shape[1]) / float(stream['info']['nominal_srate'][0])
        # 채널 이름 추출 
        ch_names = [ch['label'][0] for ch in stream['info']['desc'][0]['channels'][0]['channel']]

# 모든 채널을 EEG 타입으로 설정
ch_types = ['eeg'] * len(ch_names) 

# 샘플링 빈도는 데이터에 맞게 설정
sfreq = 100

# MNE 정보 객체 생성
info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)

# MNE RawArray 객체 생성
raw = mne.io.RawArray(eeg_data, info)

# 이벤트 정보 추출
events, event_ids = mne.events_from_annotations(raw)

# 채널 선택
picks = mne.pick_types(raw.info, eeg=True)

# 데이터 시각화
raw.plot(events=events, scalings='auto', picks=picks, block=True, n_channels=len(ch_names))