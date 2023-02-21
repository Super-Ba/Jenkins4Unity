# Jenkins4Unity

젠킨스를 사용한 유니티 윈도우 빌드를 위한 빌드 설정 및 도구

유니티 빌드 스크립트와  
ZipAndUpload 로 구성


### 프로세스 요약

1. 젠킨스 Job 시작
2. 유니티 빌드 스크립트 실행
3. 빌드 후 저장
4. ZipAndUpload 파이썬 실행
5. 빌드 압축 후 구글 드라이브 업로드


<br/>

# 사용법

<br/>

## 젠킨스 빌드 스텝 설정

<br/>

***자세한 젠킨스 설정법은 여기서 다루지 않음***

### 1. Invoke Unity3d Editor

 젠킨스 Unuty3d plugin을 통해 유니티 빌드 스크립트 호출  
  `-quit -batchmode -logfile "로그파일 경로" -executeMethod Builder.Build`
 
### 2. Execute Windows batch command

 배치 커맨드로 파이썬(ZipAndUpload) 실행  
 필요한 패키지도 같이 설치

 ```
"파이썬 경로.exe" -m pip --version
"파이썬 경로.exe" -m pip install --upgrade google-api-python-client
"파이썬 경로.exe" -m pip install --user google-auth-oauthlib

"파이썬 경로.exe" "C:\ZipAndUpload\zipAndUpload.py" 
 ```

## 유니티 빌드 설정

### 1. `BuildSetting.config` 에 빌드가 저장될 경로 입력
 경로는 ZipAndUpload의 buildPath와 같게 설정  
 `BuildSetting.config`는 유니티 프로젝트 경로에 저장
 
### 2. `Builder.cs` 를 Editor폴더에 추가
 상단 메뉴 아이템에 "Build/빌드하기"를 눌러 테스트

<br/>

## ZipAndUpload 설정

### 1. `credentials.json` 설정

 ***자세한 구글 api 설정은 여기서 다루지 않음***

 구글 api OAuth 클라이언트 ID Json 파일을 다운로드 합니다.  
 <https://console.cloud.google.com/apis/credentials>

 다운받은 Json 파일의 이름을 `credentials.json`으로 변경 후 **ZipAndUpload** 폴더에 추가합니다.

<br/>

### 2. `setting.ini` 설정

 **buildPath** : 빌드가 저장되어 있는 폴더 (유니티 `BuildSetting.config` 경로와 같게 설정)  
 **googleDrivePath** : 빌드를 업로드할 구글 드라이브 폴더 ID

> **폴더 ID** : 구글 드라이브 url의 끝 부분


<br/>

### 3. ZipAndUpload 실행 

 **zipAndUpload.py**를 한번 실행해 `token.json` 를 생성합니다.

