from gpt.exam import ShortAnswerExam, MultipleChoiceExam, EssayQuestionExam
import json

# 파일경로를 입력해주세요
# enter the file path
# filepath = "C:/GitProject/ExamGPT/testfiles/kt_info.txt"
filepath = "C:/GitProject/ExamGPT/testfiles/news.txt"
# filepath = "C:/GitProject/ExamGPT/testfiles/flask_pdf.pdf"

# 1. 객관식 문제 dictionary 예제
# 1. Example of Multiple Choice Question dictionary
# multchoice = MultipleChoiceExam(filepath)
# json_string = multchoice.get()
# json_data = json.loads(json_string)
# print(json_data)

# 2. 단답형 문제 dictionary 예제
# 2. Example of Short Answer Question dictionary
# shortanswer = ShortAnswerExam(filepath)
# json_string = shortanswer.get()
# json_data = json.loads(json_string)
# print(json_data)

# 3. 서술형 문제 dictionary 예제
# 3. Example of Essay Question dictionary
# essay = EssayQuestionExam(filepath)
# json_string = essay.get()
# json_data = json.loads(json_string)
# print(json_data)