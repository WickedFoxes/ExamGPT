from datetime import datetime
from flask import Blueprint, render_template, request, url_for, g, flash, send_file
from werkzeug.utils import redirect, secure_filename

from .. import db
from flask import current_app

from ept.models import Question
from ept.forms import QuestionForm
from ept import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, TOKEN_LIMIT

import os
import uuid
import json
import base64

from tikaparser.tika import Tika
from gpt.GPT import Token
from gpt.contentcheck import ContentCheck, ImageInfo

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def _list():
    current_user = g.user

    if current_user:
    # 현재 로그인한 사용자의 질문만 가져옴
        question_list = Question.query.filter_by(user=g.user).order_by(Question.create_date).all()
        return render_template('question/question_list.html', question_list=question_list)
    else:
        return redirect(url_for('auth.login'))


@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        return redirect(url_for('main.error'))
    return render_template('question/question_detail.html', question=question)

def allowed_file(filename):
    # 파일 확장자가 허용된 확장자인지 확인
    for ext in ALLOWED_EXTENSIONS:
        if(ext in filename): return True
    return False

@bp.route('/create/', methods=('GET', 'POST'))
def create():    
    form = QuestionForm()

    if form.validate_on_submit():
        subject = form.subject.data
        file_content = form.fileContent.data

        uploadfilepath = UPLOAD_FOLDER+"/"+str(uuid.uuid4())
        file_content.save(uploadfilepath)
        
        tika = Tika(uploadfilepath)
        file_type = tika.get_type()
        print(file_type)

        # file type check
        if not allowed_file(file_type):
            flash("Only PDF or HTML or TXT or PNG or MSOffice file formats are allowed.")
            if os.path.isfile(uploadfilepath):
                os.remove(uploadfilepath)
            return render_template('question/question_form.html', form=form)

        # file text token check
        imgflag = False
        for imgtype in ['image/png', 'image/jpeg']:
            if(imgtype in file_type): imgflag = True
        
        file_content_text = None
        if imgflag:
            fdata = open(uploadfilepath, 'rb').read()
            base64_str  = base64.b64encode(fdata).decode('utf-8')
            base64_url = f"data:image/jpeg;base64,{base64_str}"
            file_content_text = ImageInfo(base64_url).get_from_img()
        else:
            file_content_text = tika.get()

        token_count = Token(file_content_text).gpt4_token_count()
        if token_count > TOKEN_LIMIT:
            flash("The document contains "+str(token_count)+" tokens. ExamGPT limits text in documents to "+str(TOKEN_LIMIT)+" tokens.")
            if os.path.isfile(uploadfilepath):
                os.remove(uploadfilepath)
            return render_template('question/question_form.html', form=form)

        # file text content check
        contentcheck = ContentCheck(file_content_text)
        contentcheck_string = contentcheck.get()
        contentcheck_data = json.loads(contentcheck_string)
        if(contentcheck_data['content_safe'] == 'false'
           or contentcheck_data['XSS_safe'] == 'false' 
           or contentcheck_data['prompt_safe'] == 'false'):
            flash(contentcheck_data['comment'])
            if os.path.isfile(uploadfilepath):
                os.remove(uploadfilepath)
            return render_template('question/question_form.html', form=form)

        # add db data
        new_file = Question(subject=subject, file_text=file_content_text, create_date=datetime.now(), user=g.user)
        db.session.add(new_file)
        db.session.commit()

        return redirect(url_for('main.index'))

    return render_template('question/question_form.html', form=form)
        
        
        
# @bp.route('/edit/', methods=('GET', 'POST'))
# def edit():
#     form = QuestionForm()
#     question_list = Question.query.order_by(Question.create_date)
#     if request.method == 'POST' and form.validate_on_submit():
#         question = Question(subject=form.subject.data, fileContent=form.fileContent.data, create_date=datetime.now())
#         db.session.add(question)
#         db.session.commit()
#         return redirect(url_for('main.index'))
#     return render_template('question/question_edit.html', form=form, question_list=question_list)
