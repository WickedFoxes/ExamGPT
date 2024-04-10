from gpt.GPT import GPT
from tikaparser.tika import Tika

class Exam:
    def __init__(self, filepath):
        self.filepath = filepath
        self.tika = Tika(filepath)
        self.content = self.tika.get()
        self.gpt = GPT()
    
    def get(self):
        self.gpt.add_message("user", self.content)
        return self.gpt.get_gpt4_json()
    
    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")

class MultipleChoiceExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", self.readPrompt("exam/prompt/MultipleChoiceExam.prompt"))

class ShortAnswerExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", self.readPrompt("exam/prompt/ShortAnswerExam.prompt"))

class EssayQuestionExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", self.readPrompt("exam/prompt/EssayQuestionExam.prompt"))