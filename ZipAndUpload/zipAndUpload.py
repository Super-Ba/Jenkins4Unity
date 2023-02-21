import os
import os.path
import zipfile
import shutil
import configparser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


REAL_PATH = os.path.dirname(os.path.realpath(__file__))

config = configparser.ConfigParser()
config.read(REAL_PATH + '/setting.ini')

BUILDS_PATH = config['PATH']['buildPath']
BUILDS_GOOGLEDRIVE_PATH = config['PATH']['googleDrivePath']



# .zip 파일이 아닌 가장 최신의 파일을 찾아 압축하고 원래 폴더 삭제

target = sorted(os.listdir(BUILDS_PATH), reverse=True)[0]

if '.zip' in target:
    print("압축 파일이 이미 존재합니다. : " + target)
    quit()
    

targetFolder = BUILDS_PATH + '/' + target

fantasy_zip = zipfile.ZipFile(targetFolder + '.zip', 'w')
for folder, subfolders, files in os.walk(targetFolder):
    for file in files:
        fantasy_zip.write(os.path.join(folder, file), os.path.relpath(
            os.path.join(folder, file), targetFolder), compress_type=zipfile.ZIP_DEFLATED)
fantasy_zip.close()

shutil.rmtree(BUILDS_PATH + '/' + target)

print("빌드 압축 성공 : " + target)



# 구글 드라이브 업로드

SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = None

if os.path.exists(REAL_PATH + "/token.json"):
    creds = Credentials.from_authorized_user_file(REAL_PATH + "/token.json", SCOPES)

if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            REAL_PATH + "/credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    with open(REAL_PATH + '/token.json', 'w') as token:
        token.write(creds.to_json())


try:
    # 파일을 구글드라이브에 업로드하기

    service = build("drive", "v3", credentials=creds)
    
    file_metadata = {
        "name": target,
        "parents": [BUILDS_GOOGLEDRIVE_PATH]
    }

    data = MediaFileUpload(BUILDS_PATH + '/' + target + ".zip")
    upload_file = service.files().create(
        body=file_metadata, media_body=data, fields="id").execute()
    
    print("파일 업로드 성공 : " + target)

except HttpError as e:
    print("파일 업로드 실패 : " + str(e))
