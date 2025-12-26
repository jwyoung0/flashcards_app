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

    # Pre-check the checkbox for GET requests
    if request.method == 'GET':
        form.continue_adding.data = True

    if form.validate_on_submit():
        # Save the question
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

        # Check if user wants to continue adding
        if form.continue_adding.data:
            # Use redirect to clear the form (PRG pattern)
            return redirect(url_for('add_question', set_id=set_id, added=1))

        # Otherwise, go back to set detail page
        return redirect(url_for('set_detail', set_id=set_id))

    # Show success message if redirected
    message = None
    if request.args.get('added') == '1':
        message = "Question added!"

    return render_template('add_question.html', form=form, set=flashcard_set, message=message)



# Take quiz
@app.route('/set/<int:set_id>/quiz', methods=['GET','POST'])
def take_quiz(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    num_questions = session.get('num_questions', 5)

    # --- GET: select and store quiz questions ---
    if request.method == "GET":
        questions = random.sample(
            flashcard_set.questions,
        min(num_questions, len(flashcard_set.questions))
        )
        session['quiz_question_ids'] = [q.id for q in questions]

        return render_template(
            'quiz.html',
            set=flashcard_set,
            questions=questions,
            finished=False
        )

    # --- POST: load same questions and score ---
    question_ids = session.get('quiz_question_ids', [])
    questions = Question.query.filter(Question.id.in_(question_ids)).all()

    score = 0
    for q in questions:
        if request.form.get(str(q.id)) == q.correct_option:
            score += 1
    
    return render_template(
        'quiz.html', 
        set=flashcard_set, questions=questions, 
        score=score, 
        finished=True
    )


# Settings page
@app.route('/settings', methods=['GET','POST'])
def settings():
    if request.method == 'POST':
        session['num_questions'] = int(request.form['num_questions'])
        return redirect(url_for('index'))
    num_questions = session.get('num_questions', 5)
    return render_template('settings.html', num_questions=num_questions)

# --- Flashcard Set CRUD ---

# Edit set
@app.route('/set/<int:set_id>/edit', methods=['GET','POST'])
def edit_set(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    form = FlashcardSetForm(obj=flashcard_set)
    if form.validate_on_submit():
        flashcard_set.title = form.title.data
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_set.html', form=form, edit=True)

# Delete set
@app.route('/set/<int:set_id>/delete', methods=['POST'])
def delete_set(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    db.session.delete(flashcard_set)
    db.session.commit()
    return redirect(url_for('index'))

# --- Question CRUD ---

# Edit question
@app.route('/question/<int:question_id>/edit', methods=['GET','POST'])
def edit_question(question_id):
    question = Question.query.get_or_404(question_id)
    form = QuestionForm(obj=question)
    if form.validate_on_submit():
        question.question_text = form.question_text.data
        question.option_a = form.option_a.data
        question.option_b = form.option_b.data
        question.option_c = form.option_c.data
        question.option_d = form.option_d.data
        question.correct_option = form.correct_option.data
        db.session.commit()
        return redirect(url_for('set_detail', set_id=question.set_id))
    return render_template('add_question.html', form=form, set=question.set, edit=True)

# Delete question
@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    set_id = question.set_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('set_detail', set_id=set_id))

if __name__ == '__main__':
    app.run(debug=True)
