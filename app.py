from flask import Flask, render_template, redirect, url_for, request, session
from config import Config
from models import db, FlashcardSet, Question
from forms import FlashcardSetForm, QuestionForm
import random

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

# Home page: list all sets
@app.route('/')
def index():
    sets = FlashcardSet.query.all()
    return render_template('index.html', sets=sets)

# Create new flashcard set
@app.route('/create_set', methods=['GET', 'POST'])
def create_set():
    form = FlashcardSetForm()
    if form.validate_on_submit():
        new_set = FlashcardSet(title=form.title.data)
        db.session.add(new_set)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_set.html', form=form)

# Flashcard set detail + list questions
@app.route('/set/<int:set_id>')
def set_detail(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    return render_template('set_detail.html', set=flashcard_set)

# Add question to set
@app.route('/set/<int:set_id>/add_question', methods=['GET','POST'])
def add_question(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    form = QuestionForm()
    if form.validate_on_submit():
        q = Question(
            set=flashcard_set,
            question_text=form.question_text.data,
            option_a=form.option_a.data,
            option_b=form.option_b.data,
            option_c=form.option_c.data,
            option_d=form.option_d.data,
            correct_option=form.correct_option.data
        )
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('set_detail', set_id=set_id))
    return render_template('add_question.html', form=form, set=flashcard_set)

# Take quiz
@app.route('/set/<int:set_id>/quiz', methods=['GET','POST'])
def take_quiz(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    num_questions = session.get('num_questions', 5)
    questions = random.sample(flashcard_set.questions, min(num_questions, len(flashcard_set.questions)))

    if request.method == 'POST':
        score = 0
        for q in questions:
            if request.form.get(str(q.id)) == q.correct_option:
                score += 1
        return render_template('quiz.html', set=flashcard_set, questions=questions, score=score, finished=True)
    return render_template('quiz.html', set=flashcard_set, questions=questions, finished=False)

# Settings page
@app.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        session['num_questions'] = int(request.form['num_questions'])
        return redirect(url_for('index'))
    num_questions = session.get('num_questions', 5)
    return render_template('settings.html', num_questions=num_questions)

if __name__ == '__main__':
    app.run(debug=True)
