from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class FlashcardSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    questions = db.relationship('Question', backref='set', cascade="all, delete-orphan")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_id = db.Column(db.Integer, db.ForeignKey('flashcard_set.id'), nullable=False)
    question_text = db.Column(db.String(200), nullable=False)
    option_a = db.Column(db.String(100), nullable=False)
    option_b = db.Column(db.String(100), nullable=False)
    option_c = db.Column(db.String(100), nullable=False)
    option_d = db.Column(db.String(100), nullable=False)
    correct_option = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'

    def get_option_text(self, letter):
        return {
            "A": self.option_a,
            "B": self.option_b,
            "C": self.option_c,
            "D": self.option_d,
        }.get(letter)