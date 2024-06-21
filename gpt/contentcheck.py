from gpt.GPT import GPT

class ContentCheck:
    def __init__(self, content):
        self.content = content
        self.gpt = GPT()
        self.gpt.add_message("system", self.readPrompt("gpt/prompt/ContentCheck.prompt"))
    
    def get(self):
        self.gpt.add_message("user", self.content)
        return self.gpt.get_gpt4_json()
    
    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")

class ImageInfo:
    def __init__(self, imgcontent):
        self.content = imgcontent
        self.gpt = GPT()
        self.gpt.add_vision_message("user", "text", self.readPrompt("gpt/prompt/ImageInfo.prompt"))
    
    def get_from_img(self):
        self.gpt.add_vision_message("user", "image_url", self.content)
        return self.gpt.get_gpt4_vision()
    
    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")