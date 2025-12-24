from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class FlashcardSetForm(FlaskForm):
    title = StringField('Set Title', validators=[DataRequired()])
    submit = SubmitField('Create Set')

class QuestionForm(FlaskForm):
    question_text = StringField('Question', validators=[DataRequired()])
    option_a = StringField('Option A', validators=[DataRequired()])
    option_b = StringField('Option B', validators=[DataRequired()])
    option_c = StringField('Option C', validators=[DataRequired()])
    option_d = StringField('Option D', validators=[DataRequired()])
    correct_option = SelectField('Correct Option', choices=[('A','A'),('B','B'),('C','C'),('D','D')], validators=[DataRequired()])
    submit = SubmitField('Add Question')
