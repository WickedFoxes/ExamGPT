from exam.GPT import GPT
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

class MultipleChoiceExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", "너는 텍스트를 읽고, 객관식 문제를 json 형태로 내주는 기계가 될거야. 택스트 내용을 받고 아래 규칙에 따라 json 형식으로 객관식 문제를 만들어 줘야 해.")
        self.gpt.add_message("system", "json은 {'question' : '', 'answer' : 0, 'comment' : ''}의 형태로 작성해")
        self.gpt.add_message("system", "json에 'question', 'answer', 'comment'이외의 key를 만들지 마")
        self.gpt.add_message("system", "question에서 문제와 선택지를 만들어줘. 선택지는 반드시 5개야.")
        self.gpt.add_message("system", "예시 : {'question' : '이건 넌센스 문제입니다. 타이타닉의 구명보트는 몇 명이 탈수 있을까요?\n 1. 1명\n 2. 3명\n 3.5명\n 4.7명\n 5.9명'}")
        self.gpt.add_message("system", "answer에서 선택지 중 답이 몇 번인지 알려줘.")
        self.gpt.add_message("system", "예시 : {'answer' : '5번'}")
        self.gpt.add_message("system", "comment에서 question과 answer에 대한 해설을 작성해줘. 각 선택지마다 어떤 이유로 정답이 맞고, 정답이 아닌지 설명해 줘야 해.")
        self.gpt.add_message("system", "예시 : {'comment' : '구명조끼에서 \'구명\'은 \'9명\'으로 해석될 수 있습니다. 따라서 정답은 5번 9명입니다.'}")
        self.gpt.add_message("system", "question과 comment의 내용은 markdown 형식을 갖춰서 쉽게 이해할 수 있도록 작성해줘.")
        self.gpt.add_message("system", "반드시 한국어로 작성되어야 해")
        self.gpt.add_message("assistant", "{ 'question'  : '다음 중 삼각형의 특징이 아닌 것을 고르시오.\n\
        1. 변이 4개이다.\n\
        2. 내각의 합이 180도이다.\n\
        3. 2변의 길이의 합은 항상 다른 한 변의 길이보다 크거나 같다.\n\
        4. 삼각형의 어떤 각의 외각은 그 각을 제외한 다른 두 각의 합과 같다.\n\
        5. 각이 3개있다.',\
        'answer' : '1번' ,\
        'comment' :\ '삼각형의 특징은 다음과 같습니다.\
        \'\'\'\n\
        - 세 내각의 합은 180도이다. \n\
        - 삼각형의 어떤 각의 외각은 그 각을 제외한 다른 두 각의 합과 같다.\n\
        - 그 어떤 삼각형도 어느 한 변의 길이가 나머지 두 변의 길이를 합한 것보다 길거나 같을 수 없다. \n\
        \'\'\'\n\
        따라서 1번 \'변이 4개이다\'는 삼각형의 특징이 아닙니다.'}")
        self.gpt.add_message("assistant", "{ 'question'  : '4.19 혁명의 직접적인 원인으로 올바른 것을 고르시오.\n\
        1. 유신체제\n\
        2. 4.3 사건\n\
        3. 5.16 군사정변\n\
        4. 10.26 사태\n\
        5. 3.15 부정선거',\
        'answer' : '5번' ,\
        'comment' : 4·19 혁명은 3.15 부정선거를 계기로 시작되었습니다. 3.15 부정선거에 항거하는 시위가 4.19 혁명의 서막이 되었고, 이승만 대통령의 자유당 정권이 저지른 3.15 부정선거에 시민들이 항거하여 대대적으로 일어난 이 시위는 전국으로 확산되었습니다. \
        따라서 5번 \'3.15 부정선거\'가 정답입니다.'}")

class ShortAnswerExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", "너는 텍스트를 읽고, 단답식 문제를 json 형태로 내주는 기계가 될거야. 택스트 내용을 받고 아래 규칙에 따라 json 형식으로 단답식 문제를 만들어 줘야 해.")
        self.gpt.add_message("system", "json은 {'question' : '', 'answer' : '', 'comment' : ''}의 형태로 작성해")
        self.gpt.add_message("system", "json에 'question', 'answer', 'comment'이외의 key를 만들지 마")
        self.gpt.add_message("system", "question에서 문제를 만들어줘.")
        self.gpt.add_message("system", "예시 : {'question' : '넌센스 문제입니다. 타이타닉의 구명보트는 몇 명이 탈 수 있을까요?'}")
        self.gpt.add_message("system", "answer에서 정답을 단답으로 알려줘. 숫자 또는 단어가 답이 되야해. 문장이 아니야.")
        self.gpt.add_message("system", "예시 : {'answer' : '5명'}")
        self.gpt.add_message("system", "comment에서 question과 answer에 대한 해설을 작성해줘. 어떤 이유로 문제의 정답이 이것인지. 설명해야 해.")
        self.gpt.add_message("system", "예시 : {'comment' : '구명조끼에서 \'구명\'은 \'9명\'으로 해석될 수 있습니다. 따라서 정답은 5명입니다.'}")
        self.gpt.add_message("system", "question과 comment의 내용은 markdown 형식을 갖춰서 쉽게 이해할 수 있도록 작성해줘.")
        self.gpt.add_message("system", "반드시 한국어로 작성되어야 해")
        self.gpt.add_message("assistant", "{ 'question'  : '여기 직각 삼각형이 있습니다. 삼각형의 밑변의 길이는 3cm, 높이의 길이는 4cm입니다.\n\
        이 때 빗변의 길이를 구하시오.',\
        'answer' : '5cm' ,\
        'comment' :\ '피타고라스의 정리에 따라. 직각삼각형에서 빗변 길이의 제곱은 빗변을 제외한 두 변의 각각 제곱의 합과 같습니다.\n 따라서 아래와 같은 풀이가 나옵니다.\n\
        \'\'\'\n\
        3^2 + 4^2 = 9 + 16 = 25\
        5^2 = 25\
        \'\'\'\n\
        따라서 정답은 5cm입니다.'}")
        self.gpt.add_message("assistant", "{ 'question'  : '4.19 혁명의 직접적인 원인은 무엇인가요?',\n\
        'answer' : '3.15 부정선거' ,\
        'comment' : '4.19 혁명은 1960년 4월 19일에 발생한 대한민국의 민주주의를 위한 대규모 항쟁입니다. 이 혁명의 직접적인 원인은 1960년 3월 15일에 치러진 대통령 선거에서 발생한 부정선거와 이에 대한 항의 시위가 격화되면서 발생했습니다.\n\
                    당시 이승만 대통령의 정부는 장기 집권을 목표로 선거 부정과 같은 여러 방법을 사용하여 권력을 유지하려 했습니다. 특히, 3.15 부정선거는 광범위한 선거 조작을 포함하고 있었으며, 이는 대학생과 일반 시민들 사이의 광범위한 불만을 야기했습니다.\n\
                    이러한 불만은 4월 19일 서울에서 시작된 대규모 시위로 이어졌고, 시위는 전국으로 확산되었습니다. 정부의 강경한 진압에도 불구하고, 시위는 계속되었고, 결국 이승만 대통령은 하야를 발표하고 국외로 망명하게 됩니다.'}")

class EssayQuestionExam(Exam):
    def __init__(self, filepath):
        super().__init__(filepath)
        self.gpt.add_message("system", "너는 텍스트를 읽고, 서술형 문제를 json 형태로 내주는 기계가 될거야. 택스트 내용을 받고 아래 규칙에 따라 json 형식으로 서술형 문제를 만들어 줘야 해.")
        self.gpt.add_message("system", "json은 {'question' : '', 'answer' : '', 'comment' : ''}의 형태로 작성해")
        self.gpt.add_message("system", "json에 'question', 'answer', 'comment'이외의 key를 만들지 마")
        self.gpt.add_message("system", "question에서 문제를 만들어줘.")
        self.gpt.add_message("system", "예시 : {'question' : '1에서 100까지의 수 중에서 짝수들의 합을 구하는 방법을 등차수열로 설명하고 합을 구하시오.'}")
        self.gpt.add_message("system", "answer에서 정답을 서술해줘. 정답은 완성된 문장이 되야해.")
        self.gpt.add_message("system", "예시 : {'answer' : '\
                             # 등차수열의 합을 계산하기 위한 변수 정의\n\
                             a1 = 2  # 첫 번째 짝수\n\
                             an = 100  # 마지막 짝수\n\
                             n = (an / 2)  # 짝수의 개수\n\
                             # 등차수열의 합 공식 적용\n\
                             Sn = (n / 2) * (a1 + an)\n\
                             Sn = (100 / 2) * (2 + 100) = 2550\
                             '}")
        self.gpt.add_message("system", "comment에서 question과 answer에 대한 해설을 작성해줘.")
        self.gpt.add_message("system", "comment에서 출제 의도 및 문제 해설을 해야 해. 또한 어떤 평가 기준을 가지고 있는지 설명해야 해.")
        self.gpt.add_message("system", "예시 : {'comment' : '\
                             1에서 100까지의 짝수들의 합을 구하는 방법에는 몇 가지가 있지만, 가장 단순하고 효율적인 방법 중 하나는 등차수열의 합 공식을 사용하는 것입니다. \
                             등차수열은 연속되는 두 항의 차이가 일정한 수열을 말합니다. 1에서 100까지의 짝수들은 2, 4, 6, ..., 100으로 이루어진 등차수열이며, 이때의 공차는 2입니다.\n\n\
                             등차수열의 합 Sn을 구하는 공식은 다음과 같습니다.\n\
                             \'\'\' Sn=2n x (a1+an) \'\'\'\n\
                             짝수의 개수 n을 구하기 위해선 100을 2로 나눈 후, 1을 더합니다. \
                             왜냐하면 1부터 100까지의 범위에서 첫 번째 짝수는 2이고, 이것을 포함하여 계산해야 하기 때문입니다.\
                             \'\'\'\n\
                             # 등차수열의 합을 계산하기 위한 변수 정의\n\
                             a1 = 2  # 첫 번째 짝수\n\
                             an = 100  # 마지막 짝수\n\
                             n = (an / 2)  # 짝수의 개수\n\
                             # 등차수열의 합 공식 적용\n\
                             Sn = (n / 2) * (a1 + an)\n\
                             Sn = (100 / 2) * (2 + 100) = 2550\
                             \'\'\'\n\
                             따라서 1에서 100까지의 수 중에서 짝수들의 합은 2,550입니다.\
                             '}")
        self.gpt.add_message("system", "question과 comment의 내용은 markdown 형식을 갖춰서 쉽게 이해할 수 있도록 작성해줘.")
        self.gpt.add_message("system", "반드시 한국어로 작성되어야 해")
        self.gpt.add_message("assistant", "{ 'question'  : '청동기 시대에 커다란 돌을 쌓아 만든 족장의 무덤을 무엇이라고 하는가',\
        'answer' : '\
        청동기 시대에 커다란 돌을 쌓아 만든 족장의 무덤을 \"돌무덤\" 혹은 \"고인돌\"이라고 합니다.\n\
        고인돌은 사회적 지위가 높은 사람들의 무덤으로, 큰 돌판을 지탱돌 위에 얹어 만든 구조물입니다.\n\
        이 구조물은 주로 청동기 시대에 건설되었으며, 고대 사회의 장례 문화와 사회 구조를 이해하는 데 중요한 역할을 합니다.\
        ' ,\
        'comment' : '\
        - 고인돌은 청동기시대의 대표적인 무덤으로, 지상에 드러나 있는 덮개돌 밑에 받침돌로 널돌이나 자연석을 고이거나, 주검을 안치한 매장 시설이 있는 구조입니다.\n\
        - 고인돌은 계급 분화가 시작된 청동기 시대에 주로 만들어졌으며, 주로 경제력이 있거나 정치권력을 가진 지배층의 무덤으로 추정됩니다.\n\
        - 고인돌은 전 세계적으로 약 6만여 기가 분포해 있으며 우리나라에는 남·북한 모두 합쳐 3만 기 정도가 있습니다.\n\
        - 고창, 화순, 강화의 고인돌 유적은 고인돌 문화의 형성 과정과 함께 한국 청동기시대의 사회구조 및 동북아시아 선사시대의 문화 교류를 연구하는 데 매우 중요합니다.\n\
        '}")
        self.gpt.add_message("assistant", "{ 'question'  : '\
                             (가)에서 말한 \'새로운 연대 개념\'의 의미를 살려 바람직한 공동체에 대한 의견을 밝히시오\n\
                                (가) 사람들은 사회 응집을 유지하기 위해 모두가 똑같은 사람이 되기를 요구하기도 한다. 그때 각자의 개성\
                                은 은폐되거나 사라지고, 우리는 겨우 목숨을 부지하는 단순한 집합적 생명체가 된다. 그렇게 뭉친 사회적 구\
                                성원들은 마치 무기체의 분자들처럼 개성을 유보할 때만 공동의 행동을 취할 수 있다. 이러한 형태의 연대를 \
                                기계적 연대라고 부른다. 이와 반대로 분업의 진전과 함께 나타나는 연대가 있다. 기계적 연대는 개인들이 \
                                서로 유사할 것을 전제로 하지만, 분업에 의한 유기적 연대는 개인들이 서로 다르면서도 호혜적으로 공존하는 \
                                것을 전제로 한다. 기계적 연대는 개인이 집단에 일방적으로 흡수될 때에만 가능하지만, 유기적 연대는 각 개\
                                인이 고유한 행동 영역을 가지고 있을 때만 가능하다. 사회의 영역이 확장되고 그 구조가 고도화될수록 호혜적 \
                                공존을 바탕으로 한 연대가 절실해진다. 이러한 \'새로운 연대\'를 통해 생산적이고 지속 가능한 사회적 응집이 가\
                                능해지기 때문이다.\
                             ',\
                            'answer' : '\
                            제시문 (가)에서 강조하는 \'새로운 연대\'란 사회 구성원 모두가 각자의 개성을 고유하게 유지한 채 공감과 소통의 공존 가능성을 \
                            가지는 경우를 말하고 있다. 가령 분업에 기초한 호혜적 공존 가능성이 그러한 공동체의 모습을 확연하게 보여주는데, 이는 사회의 \
                            영역이 확장되어가고 구조가 고도화되는 흐름에 대한 자연스러운 연대의 원리라고 할 수 있다. 그것을 일러 제시문은 \'유기적 연대\' \
                            라고 지칭하고 있다.\
                            ' ,\
                            'comment' : '\
                             구성과 전개\n\
                             -(가)의 키워드를 충실하게 설명해야 한다.\n\n\
                            문장과 표현\n\
                            - 정확한 단어 및 표현 선택, 자연스러운 문장 구성, 문장 및 단락 사이의 유기적 연결을 평가해야 한다.\n\n\
                             유의 사항\n\
                            - 주어진 글에 나타난 구절을 그대로 반복해서 사용하고 나열하는 것은 감점 요인이다.\n\
                            - 원고지 사용법과 어문 규정을 적용하되, 감점 처리는 두드러지게 틀린 경우에 반영한다.\n\
                            - ‘서론-본론-결론’의 형식을 갖추었는지의 여부는 평가에 반영하지 않는다.\n\
                            - 대응 방안에 대한 평가에서는 창의성과 논리성을 중점적으로 판단한다.\
                            '}")