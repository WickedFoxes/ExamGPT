from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g, flash
from werkzeug.utils import redirect

from .. import db
from ept.models import Question, Answer
from ept.views.auth_views import login_required

import json
from gpt.exam import MultipleChoiceExam, EssayQuestionExam, ShortAnswerExam

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/multiplechoice')
@login_required
def mult_create(question_id):
    question = Question.query.get_or_404(question_id)
    
    file_text = question.file_text
    exam_string = MultipleChoiceExam(file_text).get()
    exam_data = json.loads(exam_string)
    beginanswer = Answer(examquestion=exam_data["begin"]["question"], 
                    examcomment=exam_data["begin"]["comment"], 
                    examanswer=exam_data["begin"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=exam_data["normal"]["question"], 
                    examcomment=exam_data["normal"]["comment"], 
                    examanswer=exam_data["normal"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=exam_data["advanced"]["question"], 
                    examcomment=exam_data["advanced"]["comment"], 
                    examanswer=exam_data["advanced"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)
    
    db.session.commit()
    return render_template('question/question_detail.html', question=question)

@bp.route('/create/<int:question_id>/essayquestion')
@login_required
def essay_create(question_id):
    question = Question.query.get_or_404(question_id)
    
    file_text = question.file_text
    exam_string = EssayQuestionExam(file_text).get()
    exam_data = json.loads(exam_string)
    beginanswer = Answer(examquestion=exam_data["begin"]["question"], 
                    examcomment=exam_data["begin"]["comment"], 
                    examanswer=exam_data["begin"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=exam_data["normal"]["question"], 
                    examcomment=exam_data["normal"]["comment"], 
                    examanswer=exam_data["normal"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=exam_data["advanced"]["question"], 
                    examcomment=exam_data["advanced"]["comment"], 
                    examanswer=exam_data["advanced"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)
    
    db.session.commit()
    return render_template('question/question_detail.html', question=question)

@bp.route('/create/<int:question_id>/shortanswer')
@login_required
def short_create(question_id):
    question = Question.query.get_or_404(question_id)
    
    file_text = question.file_text
    exam_string = ShortAnswerExam(file_text).get()
    exam_data = json.loads(exam_string)
    beginanswer = Answer(examquestion=exam_data["begin"]["question"], 
                    examcomment=exam_data["begin"]["comment"], 
                    examanswer=exam_data["begin"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(beginanswer)
    normalanswer = Answer(examquestion=exam_data["normal"]["question"], 
                    examcomment=exam_data["normal"]["comment"], 
                    examanswer=exam_data["normal"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(normalanswer)
    advancedanswer = Answer(examquestion=exam_data["advanced"]["question"], 
                    examcomment=exam_data["advanced"]["comment"], 
                    examanswer=exam_data["advanced"]["answer"], 
                    create_date=datetime.now(), user=g.user)
    question.answer_set.append(advancedanswer)
    
    db.session.commit()
    return render_template('question/question_detail.html', question=question)

@bp.route('/delete/<int:answer_id>')
@login_required
def delete(answer_id):
    answer = Answer.query.get_or_404(answer_id)
    question_id = answer.question.id
    if g.user != answer.user:
        flash('삭제권한이 없습니다')
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

