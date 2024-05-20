from gpt.GPT import GPT

class Exam:
    def __init__(self, content):
        self.content = content
        self.gpt = GPT()
    
    def get(self):
        self.gpt.add_message("user", self.content)
        return self.gpt.get_gpt4_json()
    
    def get_from_img(self):
        self.gpt.add_vision_message("user", "image_url", self.content)
        return self.gpt.get_gpt4_vision()

    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")

class MultipleChoiceExam(Exam):
    def __init__(self, content):
        super().__init__(content)
        self.gpt.add_message("system", self.readPrompt("gpt/prompt/MultipleChoiceExam.prompt"))

class ShortAnswerExam(Exam):
    def __init__(self, content):
        super().__init__(content)
        self.gpt.add_message("system", self.readPrompt("gpt/prompt/ShortAnswerExam.prompt"))

class EssayQuestionExam(Exam):
    def __init__(self, content):
        super().__init__(content)
        self.gpt.add_message("system", self.readPrompt("gpt/prompt/EssayQuestionExam.prompt"))

class ReadImgExam(Exam):
    def __init__(self, content):
        super().__init__(content)
        self.gpt.add_vision_message("user", "text", self.readPrompt("gpt/prompt/ReadImgExam.prompt"))

class CustomExam(Exam):
    def __init__(self, content, htmlcontent):
        super().__init__(content)
        self.gpt.add_message("system", self.readPrompt("gpt/prompt/CustomExam.prompt"))
        self.gpt.add_message("system", "#problem written with the html tag\n\n"+htmlcontent)