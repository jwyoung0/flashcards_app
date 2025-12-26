# Flashcards App

A simple Flask web application for creating flashcard sets, adding multiple-choice questions, and taking quizzes. Users can adjust the number of questions per quiz.
---

## Features

- **Flashcard Sets**
  - Create, edit, and delete flashcard sets
  - Manage all set content from a single Edit Set page

- **Questions**
  - Add questions inline
  - Edit and delete questions
  - Multiple-choice format (A–D)

- **Quiz Mode**
  - Take a quiz from any flashcard set
  - Choose number of questions per quiz
  - Randomized question selection

- **Settings**
  - Store quiz preferences

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
│   ├── edit_set.html
│   ├── add_question.html
│   ├── quiz.html 
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
3. Manage a set from the Edit Set page:
    - Rename the set
    - Add questions inline
    - Edit or delete questions
4. Take a quiz from the set
5. Adjust quiz settings via **Settings**.

💡 Tip: Press **Ctrl + Enter** when adding questions to submit quickly.

---

## UX Enhancements

- One-page set management
- Inline question creation with instant feedback
- Card-style layout for questions
- Keyboard shortcut: **Ctrl + Enter** to add the next question
- Confirmation prompts for destructive actions

---

## Notes

* The app uses **SQLite** for the database (`flashcards.db`).

---

## License

This project is open-source and free to use.

