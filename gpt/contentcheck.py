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

class PromptAttackError(Exception):
    def __init__(self):
        super().__init__('This texts contains contents that damage the prompt')

class XSSAtackError(Exception):
    def __init__(self):
        super().__init__('This text contains content that causes cross-site scripting')

class NotExamContentError(Exception):
    def __init__(self):
        super().__init__('This text does not contain anything useful for taking the exam')

class NotClearContentError(Exception):
    def __init__(self):
        super().__init__('This text does not contain clear contents')