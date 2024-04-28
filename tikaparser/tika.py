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
        # +"\" --header \"Accept: text/html\""
        # print(cmd)
        content += subprocess.check_output(cmd, text=False, shell=True)
        return content.decode(encoding="utf-8")
    
    def get_type(self):
        doc_type_cmd = "java -jar tikaparser/lib/tika-app-2.9.1.jar -d \"" + self.filepath + "\""
        doc_type = subprocess.check_output(doc_type_cmd, text=False, shell=True)
        return doc_type.decode(encoding="utf-8")