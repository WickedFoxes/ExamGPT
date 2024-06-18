from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ept.models import Question, Answer
from ept.views.auth_views import login_required
from ept.forms import CustomForm

import json
import base64
from gpt.exam import MultipleChoiceExam, EssayQuestionExam, ShortAnswerExam, CustomExam
from bs4 import BeautifulSoup

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/custom', methods=('GET', 'POST'))
@login_required
def custom_create(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        return redirect(url_for('main.error'))
    
    form = CustomForm()
    if form.validate_on_submit():
        file_content = form.fileContent.data

        file_text = question.file_text
        base64_str  = base64.b64encode(file_content.read()).decode('utf-8')
        base64_url = f"data:image/jpeg;base64,{base64_str}"

        g.user.creating_state = True
        db.session.commit()

        # imgRead = ReadImgExam(base64_url)
        # htmlcontent = imgRead.get_from_img()

        exam_string = CustomExam(file_text, base64_url).get_from_img()
        soup = BeautifulSoup(exam_string, 'html.parser')
        print(soup)
        questions = soup.find_all("div", {"class":"question"})
        solves = soup.find_all("div", {"class":"solve"})
        answers = soup.find_all("div", {"class":"answer"})

        beginanswer = Answer(examquestion=str(questions[0]), 
                        examcomment=str(solves[0]), 
                        examanswer=str(answers[0]), 
                        create_date=datetime.now(), user=g.user)
        question.answer_set.append(beginanswer)
        normalanswer = Answer(examquestion=str(questions[1]), 
                        examcomment=str(solves[1]), 
                        examanswer=str(answers[1]), 
                        create_date=datetime.now(), user=g.user)
        question.answer_set.append(normalanswer)
        advancedanswer = Answer(examquestion=str(questions[2]), 
                        examcomment=str(solves[2]), 
                        examanswer=str(answers[2]), 
                        create_date=datetime.now(), user=g.user)
        question.answer_set.append(advancedanswer)

        g.user.creating_state = False
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    
    return render_template('question/question_custom_form.html', form=form)

@bp.route('/create/<int:question_id>/multiplechoice')
@login_required
def mult_create(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        return redirect(url_for('main.error'))
    if g.user.creating_state:
        return redirect(url_for('main.exam_create_error'))

    g.user.creating_state = True
    db.session.commit()
    
    file_text = question.file_text
    exam_string = MultipleChoiceExam(file_text).get()
    soup = BeautifulSoup(exam_string, 'html.parser')
    questions = soup.find_all("div", {"class":"question"})
    solves = soup.find_all("div", {"class":"solve"})
    answers = soup.find_all("div", {"class":"answer"})
    print(soup)

    beginanswer = Answer(examquestion=str(questions[0]), 
                    examcomment=str(solves[0]), 
                    examanswer=str(answers[0]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=str(questions[1]), 
                    examcomment=str(solves[1]), 
                    examanswer=str(answers[1]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=str(questions[2]), 
                    examcomment=str(solves[2]), 
                    examanswer=str(answers[2]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)

    g.user.creating_state = False
    db.session.commit()
    return render_template('complete.html', question=question)
    # return render_template('question/question_detail.html', question=question)

@bp.route('/create/<int:question_id>/essayquestion')
@login_required
def essay_create(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        return redirect(url_for('main.error'))
    if g.user.creating_state:
        return redirect(url_for('main.exam_create_error'))

    g.user.creating_state = True
    db.session.commit()

    file_text = question.file_text
    exam_string = EssayQuestionExam(file_text).get()
    soup = BeautifulSoup(exam_string, 'html.parser')
    questions = soup.find_all("div", {"class":"question"})
    solves = soup.find_all("div", {"class":"solve"})
    answers = soup.find_all("div", {"class":"answer"})

    beginanswer = Answer(examquestion=str(questions[0]), 
                    examcomment=str(solves[0]), 
                    examanswer=str(answers[0]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=str(questions[1]), 
                    examcomment=str(solves[1]), 
                    examanswer=str(answers[1]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=str(questions[2]), 
                    examcomment=str(solves[2]), 
                    examanswer=str(answers[2]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)

    g.user.creating_state = False
    db.session.commit()
    return render_template('complete.html', question=question)
    # return render_template('question/question_detail.html', question=question)

@bp.route('/create/<int:question_id>/shortanswer')
@login_required
def short_create(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        return redirect(url_for('main.error'))
    if g.user.creating_state:
        return redirect(url_for('main.exam_create_error'))

    g.user.creating_state = True
    db.session.commit()

    
    file_text = question.file_text
    exam_string = ShortAnswerExam(file_text).get()
    soup = BeautifulSoup(exam_string, 'html.parser')
    questions = soup.find_all("div", {"class":"question"})
    solves = soup.find_all("div", {"class":"solve"})
    answers = soup.find_all("div", {"class":"answer"})

    beginanswer = Answer(examquestion=str(questions[0]), 
                    examcomment=str(solves[0]), 
                    examanswer=str(answers[0]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=str(questions[1]), 
                    examcomment=str(solves[1]), 
                    examanswer=str(answers[1]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=str(questions[2]), 
                    examcomment=str(solves[2]), 
                    examanswer=str(answers[2]), 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)

    g.user.creating_state = False
    db.session.commit()
    return render_template('complete.html', question=question)
    # return render_template('question/question_detail.html', question=question)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        return redirect(url_for('main.error'))
    else:
        db.session.delete(answer)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))


@bp.route('/vote/<int:answer_id>/')
@login_required
def vote(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    if g.user == answer.user:
        flash('본인이 작성한 글은 추천할수 없습니다')
    else:
        answer.voter.append(g.user)
        db.session.commit()
    return redirect('{}#answer_{}'.format(
                url_for('question.detail', question_id=answer.question.id), answer.id))

