## 실험 시작 프로토콜
### 1. EEG 장치 연결
### 2. actiCHamp Connector 실행
   1. Scan for Devices - `Scan`
   2. Available Devices - `22050821` 검색될 것
   1. `Num of EEG Channels` : 채널 수에 맞게끔 지정
      1. 32채널이 아닌 경우, 채널 라벨을 직접 써줘야 함
   2. Chunk Size : `10`
   3. Base Sampling Rate : `10000`
   4. Sub Sample Divisor : `10`
   5. Base Sampling Rate / Sub Sample Divisor = `Nominal Sampling Rate` = EEG 파일 Sampling Rate
   6. `Link`
### 3. BrainVision LSL Viewer 실행
  1. Connect - **actiCHamp-22050821 (22050821) Rate = `N` Hz**
  2. Configuration에서 직접 Notch Filter 켤 수 있음
### 4. Lab Recorder 실행
  1. 패러다임 코드 실행
  2. Update - `trigger_stream` 검색된 것 확인
  3. `actiCHamp-22050821 (BCIcenter)` , `trigger_stream` 선택
  4. `Study Root`: 파일이 저장될 디렉터리
  5. 피험자, 세션 지정
  6. `Start` 누르면 바로 레코딩 시작

### 다운로드
- **BrainVision LSL Viewer**
    
    [https://www.brainproducts.com/downloads/more-software](https://www.brainproducts.com/downloads/more-software/)
    
- **LSL-actiCHamp**
     
    https://github.com/brain-products/LSL-actiCHamp 
    
- **LabRecorder**
    
    https://github.com/labstreaminglayer/App-LabRecorder
    
- pip 패키지 설치
    ```
    pip install -r requirements.txt
    ```
    
    https://github.com/labstreaminglayer/pylsl 
    ```bash
    pip install pylsl
    ```
    
    https://github.com/labstreaminglayer/pylsl/tree/master/pylsl/examples 
