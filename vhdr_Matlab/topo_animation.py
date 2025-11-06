import numpy as np
import mne
from scipy.io import loadmat
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

file_path = '/data.npz'

# .npz 파일에서 데이터 로드
with np.load(file_path) as data:
    X = data['X']  # EEG 데이터
    y = data['y']  # 이벤트 ID

# 채널 위치 정보 불러오기
chanlocs_path = '/chanlocs.mat'
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

montage_ch_pos = {ch[0]: (ch[1], ch[2], ch[3]) for ch in channels}
montage = mne.channels.make_dig_montage(ch_pos=montage_ch_pos)

info = mne.create_info(montage.ch_names, sfreq=250, ch_types='eeg')
info.set_montage(montage)

# 첫 번째 이벤트의 데이터로 EvokedArray 객체 생성
evoked = mne.EvokedArray(X[0], info)

times = np.linspace(0, len(X[0])/250, len(X[0])) # 시간 배열 생성 (데이터에 따라 조정 필요)
fig, anim = evoked.animate_topomap(times=times, ch_type="eeg", frame_rate=30, blit=False)
# 저장
anim.save('topomap_animation.mp4', writer='ffmpeg', fps=30)

plt.show()