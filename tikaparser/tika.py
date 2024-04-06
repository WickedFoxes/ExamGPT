import subprocess

# tikaServerName : tika-server 연결 url
tikaServerName="http://localhost:9998/tika"
# tikaOCRLang : tika-server의 tesseract 언어 설정
tikaOCRLang="eng+kor"

class Tika:
    def __init__(self, filepath):
        self.filepath = filepath

    def get(self):
        content = b""
        cmd = "curl -T \""+ self.filepath + "\""\
				+ " \""+tikaServerName + "\""\
				+ " --header \"X-Tika-OCRLanguage: " + tikaOCRLang\
				+"\" --header \"Accept: text/plain\""
        # print(cmd)
        content += subprocess.check_output(cmd, text=False, shell=True)
        return content.decode(encoding="utf-8")