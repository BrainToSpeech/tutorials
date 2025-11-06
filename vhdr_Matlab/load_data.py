import itertools
import os
import numpy as np
import mne
from scipy.io import loadmat

# 실행 전 수정 필수
dire = '/Users/favorcat/Matlab/2_word'
save_dir = '/Users/favorcat/Matlab/artifact_remove'
subjects = ['sub4']
sessions = ['day1','day2']

chanlocs_path = '/Users/favorcat/Matlab/2_word/chanlocs.mat'
chanlocs_data = loadmat(chanlocs_path)
chanlocs = chanlocs_data['chanlocs'][0]
channels = []

# 전체 채널 위치 정보를 확인하고 Montage에 추가
for i in range(127):
  label = chanlocs[i][0][0] # label
  x = chanlocs[i][4][0][0] # x
  y = chanlocs[i][5][0][0] # y
  z = chanlocs[i][6][0][0] # z
  channels.append([label, x, y, z])
  
stim_def = [[17,21,33,37,49,53,65,69,81,85,97,101,113,117,129,133,145,149,161,165],
            ['Sad','Amused','Positive','Disappointed',
            'Peach','Mango','Strawberry','Watermelon',
            'Horse','Tiger','Buffalo','Alligator',
            'House','Notebook','Apartment','Television',
            'Death','Weather','January','Conversation']]

stim_p = [[0] * 20, ['']*20]
stim_o = [[0] * 20, ['']*20]
stim_w = [[0] * 20, ['']*20]
stim_i = [[0] * 20, ['']*20]

for i in range(len(stim_def[0])):
  # perception
  stim_p[0][i] = stim_def[0][i] 
  stim_p[1][i] = stim_def[1][i] + '_p'
  
  # overt
  stim_o[0][i] = stim_def[0][i] + 1
  stim_o[1][i] = stim_def[1][i] + '_o'
  
  # whisper
  stim_w[0][i] = stim_def[0][i] + 2
  stim_w[1][i] = stim_def[1][i] + '_w'
  
  # imagined
  stim_i[0][i] = stim_def[0][i] + 3
  stim_i[1][i] = stim_def[1][i] + '_i'

stim_all = [list(itertools.chain(stim_p[0],stim_o[0],stim_w[0],stim_i[0])),
            list(itertools.chain(stim_p[1],stim_o[1],stim_w[1],stim_i[1]))]

ival = [-1.5, 0]  # 초 단위로 변경

# load data
for sub in subjects:
  for sess in sessions:
    final_save_dir = os.path.join(save_dir, 'proc_mat', sub, sess)
    os.makedirs(final_save_dir, exist_ok=True)
    print(f'start: {sub} {sess}')
    file_dir = os.path.join(dire, sub, sess)
    files = sorted([f for f in os.listdir(file_dir) if f.endswith('.vhdr')])
    print(*files, sep='\n')

    # 파일 처리 및 경고 메시지
    if len(files) != 2:
        print('Please check the number of files')
        continue
    
    # 파일 읽기 및 데이터 처리
    # 예시: MNE 라이브러리를 사용하여 EEG 데이터 읽기
    raw = mne.io.read_raw_brainvision(os.path.join(file_dir, files[0]), preload=True)
    event_id = {label: num for label, num in zip(stim_all[1], stim_all[0])}
    events, _ = mne.events_from_annotations(raw)
    
    # 채널 선택
    picks = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False)
    raw.pick(picks[:127])
    
    # 채널 몽타주 설정
    montage_ch_pos = {ch[0]: (ch[1], ch[2], ch[3]) for ch in channels}
    montage = mne.channels.make_dig_montage(ch_pos=montage_ch_pos)
    raw.set_montage(montage)
    
    # 필터링
    raw.filter(30, 125)
    raw.notch_filter(np.array([60, 120]))

    # 재참조
    raw.set_eeg_reference('average')

    # 채널 선택 후의 새로운 picks 배열 업데이트
    picks_updated = mne.pick_types(raw.info, meg=False, eeg=True, eog=False, stim=False)

    # 이벤트 ID에 따라 에포킹
    epochs = mne.Epochs(raw, events, event_id=event_id, tmin=ival[0], tmax=ival[1], picks=picks_updated, preload=True)

    # 각 조건에 따른 에포킹 데이터 추출 및 저장
    for label, num in zip(stim_all[1], stim_all[0]):
      epo = epochs[label]
      X = epo.get_data(copy=True)
      y = epo.events[:, 2]  # 이벤트 ID
      # 데이터 저장
      np.savez(os.path.join(final_save_dir, f'data_{label}.npz'), X=X, y=y)
