from pylsl import StreamInlet, resolve_stream
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

print("Channel names:", channel_names)
print("Channel count:", len(channel_names))

# 데이터 수집을 위한 변수 초기화
all_samples = []
start_time = time.time()

# 5초 동안 데이터 수집
while time.time() - start_time < 5:
    sample, timestamp = eeg_inlet.pull_sample()
    if sample:
        all_samples.append(dict(zip(channel_names, sample)))

# 수집된 데이터 출력
for idx, data in enumerate(all_samples):
    print(f"Sample {idx + 1}: {data}")