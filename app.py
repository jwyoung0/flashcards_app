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


# ===============================
# Home
# ===============================
@app.route('/')
def index():
    sets = FlashcardSet.query.all()
    return render_template('index.html', sets=sets)


# ===============================
# Create Set
# ===============================
@app.route('/create_set', methods=['GET', 'POST'])
def create_set():
    form = FlashcardSetForm()
    if form.validate_on_submit():
        new_set = FlashcardSet(title=form.title.data)
        db.session.add(new_set)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_set.html', form=form)


# ===============================
# Edit Set (MAIN HUB)
# ===============================
@app.route('/set/<int:set_id>/edit', methods=['GET', 'POST'])
def edit_set(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)

    set_form = FlashcardSetForm(obj=flashcard_set)
    question_form = QuestionForm()

    # --- Update set title ---
    if set_form.validate_on_submit() and set_form.submit.data:
        flashcard_set.title = set_form.title.data
        db.session.commit()
        return redirect(url_for('edit_set', set_id=set_id, updated=1))

    # --- Add question ---
    if question_form.validate_on_submit():
        q = Question(
            set=flashcard_set,
            question_text=question_form.question_text.data,
            option_a=question_form.option_a.data,
            option_b=question_form.option_b.data,
            option_c=question_form.option_c.data,
            option_d=question_form.option_d.data,
            correct_option=question_form.correct_option.data
        )
        db.session.add(q)
        db.session.commit()
        return redirect(url_for('edit_set', set_id=set_id, added=1) + '#add-question')

    message = None
    if request.args.get('updated'):
        message = "Set updated successfully!"
    elif request.args.get('added'):
        message = "Question added!"

    question_form.continue_adding.data = True

    return render_template(
        'edit_set.html',
        set=flashcard_set,
        set_form=set_form,
        question_form=question_form,
        message=message
    )


# ===============================
# Delete Set
# ===============================
@app.route('/set/<int:set_id>/delete', methods=['POST'])
def delete_set(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    db.session.delete(flashcard_set)
    db.session.commit()
    return redirect(url_for('index'))


# ===============================
# Edit Question
# ===============================
@app.route('/question/<int:question_id>/edit', methods=['GET', 'POST'])
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
        return redirect(url_for('edit_set', set_id=question.set_id))

    return render_template(
        'add_question.html',
        form=form,
        set=question.set,
        edit=True
    )


# ===============================
# Delete Question
# ===============================
@app.route('/question/<int:question_id>/delete', methods=['POST'])
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    set_id = question.set_id
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('edit_set', set_id=set_id))


# ===============================
# Quiz
# ===============================
@app.route('/set/<int:set_id>/quiz', methods=['GET', 'POST'])
def take_quiz(set_id):
    flashcard_set = FlashcardSet.query.get_or_404(set_id)
    num_questions = session.get('num_questions', 5)

    if request.method == 'GET':
        # Pick random questions
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

    # POST: grading
    question_ids = session.get('quiz_question_ids', [])
    questions = Question.query.filter(Question.id.in_(question_ids)).all()

    # Build a per-question result list
    results = []
    score = 0

    for q in questions:
        selected = request.form.get(str(q.id))
        correct = q.correct_option
        is_correct = selected == correct
        if is_correct:
            score += 1

        results.append({
            'question': q,
            'selected': selected,
            'correct': correct,
            'is_correct': is_correct
        })

    return render_template(
        'quiz.html',
        set=flashcard_set,
        questions=questions,
        score=score,
        finished=True,
        results=results
    )



# ===============================
# Settings
# ===============================
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        session['num_questions'] = int(request.form['num_questions'])
        return redirect(url_for('index'))

    num_questions = session.get('num_questions', 5)
    return render_template('settings.html', num_questions=num_questions)


if __name__ == '__main__':
    app.run(debug=True)
