# Flashcards App

A simple Flask web application for creating flashcard sets, adding multiple-choice questions, and taking quizzes. Users can adjust the number of questions per quiz and choose the quiz style (all at once or one question per page).

---

## Features

- **Flashcard Sets**: Create, read, update, and delete flashcard sets.
- **Questions**: Add, edit, and delete multiple-choice questions.
- **Quiz Mode**:
  - Take a quiz from any flashcard set.
  - Choose the number of questions per quiz.
  - Quiz style: all questions at once or one question per page.
- **Settings**: Store quiz preferences in session.

---

## Project Structure

```

flashcards_app/
├── app.py
├── models.py
├── forms.py
├── config.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── create_set.html
│   ├── set_detail.html
│   ├── add_question.html
│   ├── quiz.html
│   ├── quiz_one.html
│   └── settings.html
├── static/
└── requirements.txt

````

---

## Setup

1. **Clone the repository:**

```bash
git clone https://github.com/your-username/flashcards_app.git
cd flashcards_app
````

2. **Create a virtual environment and activate it:**

```bash
python -m venv venv
# Mac/Linux
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Run the app:**

```bash
python app.py
```

5. **Open in your browser:**

[http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Dependencies

* Flask
* Flask-WTF
* WTForms
* Flask-SQLAlchemy

---

## Usage

1. Navigate to **Home** to see all flashcard sets.
2. Create a new set using **Create Set**.
3. Add multiple-choice questions to your set.
4. Take a quiz from the set, using your preferred quiz style.
5. Adjust quiz settings via **Settings**.

---

## Notes

* The app uses **SQLite** for the database (`flashcards.db`).
* Quiz settings are stored in the **session**, so they are temporary per browser session.
* Deleting a flashcard set will delete all its questions (cascade delete).

---

## License

This project is open-source and free to use.

