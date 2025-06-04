from flask import Flask, render_template, request, redirect, url_for, session, flash
import db
from main import generate_quiz
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/quizzes')
def quizzes():
    topics = db.get_topics()
    return render_template('quizzes.html', topics=topics)

@app.route('/quiz/<topic>', methods=['GET', 'POST'])
def quiz(topic):
    questions = db.get_quiz(topic)
    if request.method == 'POST':
        answers = request.form.to_dict()
        session['answers'] = answers
        return redirect(url_for('quiz_summary', topic=topic))
    if questions:
        return render_template('quiz.html', topic=topic, questions=questions)
    return render_template('create_quiz.html', topic=topic)

@app.route('/delete_quiz/<topic>')
def delete_quiz(topic):
    db.delete_quiz(topic)
    flash(f'Quiz "{topic}" deleted successfully!', 'success')
    return redirect(url_for('quizzes'))

@app.route('/create_quiz', methods=['POST'])
def create_quiz():
    new_topic = request.form.get('new_topic')
    if not new_topic:
        flash('Please enter a topic name', 'error')
        return redirect(url_for('quizzes'))
    
    try:
        quiz_data = generate_quiz(new_topic)
        if not quiz_data:
            flash('Failed to generate quiz. Please try again.', 'error')
            return redirect(url_for('quizzes'))
        
        db.create_quiz(new_topic, quiz_data)
        flash(f'Quiz on "{new_topic}" created successfully!', 'success')
        return redirect(url_for('quizzes'))
    except Exception as e:
        flash('An error occurred while creating the quiz', 'error')
        return redirect(url_for('quizzes'))

@app.route('/quiz_summary/<topic>')
def quiz_summary(topic):
    questions = db.get_quiz(topic)
    answers = session.get('answers', {})
    correct_count = 0
    attempted_count = 0
    total_questions = len(questions)

    for i, question in enumerate(questions):
        correct_answer = question['correct_answer']
        user_answer = answers.get(f'question{i+1}')
        if user_answer:
            attempted_count += 1
            if user_answer == correct_answer:
                correct_count += 1

    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    return render_template(
        'quiz_summary.html',
        topic=topic,
        questions=questions,
        answers=answers,
        correct_count=correct_count,
        attempted_count=attempted_count,
        total_questions=total_questions,
        percentage=percentage
    )

if __name__ == '__main__':
    app.run(debug=True)
