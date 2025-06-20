from django.shortcuts import render, redirect,get_object_or_404
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from .forms.signin import SignInForm
from .forms.signup import SignUpForm
from .models import Topic,Formula,Question
import random,time,re

# Sign Up View
class RegisterView(View):
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Hash password
            user.save()
            return redirect('signin')  
        return render(request, 'signup.html', {'form': form})

class SignInView(View):
    def get(self, request):
        form = SignInForm()
        return render(request, 'signin.html', {'form': form})

    def post(self, request):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home.html
            else:
                form.add_error(None, "Invalid Username or Password")

        return render(request, 'signin.html', {'form': form})


# Home View
def home_view(request):
    return render(request, 'home.html')


def topics(request):
    topics = Topic.objects.all()  # Fetch all topics from the DB
    return render(request, 'aptitude_topics.html', {'topics': topics})


def topics_detail(request, topic_id):
    topic = get_object_or_404(Topic, topic_id=topic_id)
    return render(request, 'topics_detail.html', {'topic': topic})

def formulas_page(request, topic_id):
    topic = get_object_or_404(Topic, topic_id=topic_id)
    formulas = Formula.objects.filter(topic=topic)
    return render(request, 'formulas.html', {'topic': topic, 'formulas': formulas})

import random
import re
import time
from django.shortcuts import render, redirect
from .models import Question

import re
import random

def generate_values(question_text):
    value_ranges = {
        "x": (5, 50), "y": (5, 50), "z": (1, 10), "X": (1, 20), "T": (1, 10),
        "T1": (5, 20), "T2": (5, 20), "S": (10, 120), "S1": (30, 100), "S2": (20, 90),
        "D": (50, 500), "L": (5, 100), "L1": (5, 50), "L2": (5, 50), "Lb": (1, 20),
        "A_days": (5, 30), "B_days": (5, 30), "SP": (100, 1000), "CP": (50, 900),
        "MP": (100, 1500), "P": (5, 30), "G": (5, 30)
    }

    # Find placeholders (inside {} or standalone words)
    placeholders = re.findall(r'\{?([\w]+)\}?', question_text)

    # Generate values for detected placeholders
    values = {key: random.randint(*value_ranges[key]) for key in placeholders if key in value_ranges}

    # Replace all placeholders in question_text
    for key, val in values.items():
        question_text = re.sub(rf'\b{key}\b', str(val), question_text)

    return question_text


def practice_question(request, topic_id, question_index=1):
    questions = list(Question.objects.filter(topic_id=topic_id).order_by('question_id'))  
    total_questions = len(questions)

    if not questions:
        return render(request, 'practice.html', {'error': "No questions found."})

    question_index = max(1, min(question_index, total_questions))
    question = questions[question_index - 1]  
    generated_question = generate_values(question.question_text)

    user_answer = None
    feedback = None

    if request.method == "POST":
        user_answer = request.POST.get("user_answer", "").strip()
        correct_answer = str(eval(generate_values(question.answer)))  # Evaluating the formula

        if user_answer == correct_answer:
            feedback = "Correct! 🎉"
        else:
            feedback = f"Wrong ❌. The correct answer is {correct_answer}."

    context = {
        "question": generated_question,
        "question_index": question_index,
        "total_questions": total_questions,
        "topic_id": topic_id,
        "user_answer": user_answer,
        "feedback": feedback,
    }
    return render(request, "practice.html", context)


def test_question(request, topic_id, question_index=1):
    questions = list(Question.objects.filter(topic_id=topic_id).order_by('question_id'))
    total_questions = len(questions)

    if not questions:
        return render(request, 'test.html', {'error': "No questions available."})

    question_index = max(1, min(question_index, total_questions))
    question = questions[question_index - 1]
    formatted_question = generate_values(question.question_text)  # Generate dynamic question

    if request.method == "POST":
        user_answer = request.POST.get("user_answer", "").strip()

        if question_index < total_questions:
            return redirect('test_question', topic_id=topic_id, question_index=question_index + 1)
        else:
            return redirect('test_result', topic_id=topic_id)

    context = {
        'question': formatted_question,
        'question_index': question_index,
        'total_questions': total_questions,
        'topic_id': topic_id,
        'is_last_question': question_index == total_questions,
    }

    return render(request, 'test.html', context)



import random
import json
from django.shortcuts import render

def test_result(request, topic_id):
    total_questions = 10  # Dummy total number of questions
    correct_answers = random.randint(3, total_questions)  # Random correct count
    incorrect_answers = total_questions - correct_answers  # Calculate wrong answers
    total_time = round(random.uniform(80, 150), 2)  # Simulating total time taken

    # Dummy data for time taken per question (random values)
    time_per_question = [round(random.uniform(5, 20), 2) for _ in range(total_questions)]
    
    # Dummy score calculation
    score = correct_answers * 10  # Assuming 10 points per correct answer
    
    context = {
        "score": score,
        "total_questions": total_questions,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "total_time": total_time,
        "time_per_question": json.dumps(time_per_question)  # Convert list to JSON for frontend
    }

    return render(request, 'test_result.html', context)



from django.shortcuts import render
import random
import datetime

def progress_page(request):
    total_attempted = 100
    correct_answers = 75
    incorrect_answers = total_attempted - correct_answers
    score = 80  

    today = datetime.date.today()

    # Generate Dummy Weekly Progress (Last 7 Days)
    weekly_progress = []
    for i in range(7):
        date = today - datetime.timedelta(days=i)
        attempted = random.randint(0, 5)
        correct = random.randint(0, attempted)
        weekly_progress.append({"date": date.strftime('%Y-%m-%d'), "attempted": attempted, "correct": correct})
    weekly_progress.reverse()

    # Generate Dummy Monthly Progress (Last 30 Days)
    monthly_progress = []
    for i in range(30):
        date = today - datetime.timedelta(days=i)
        attempted = random.randint(0, 10)
        correct = random.randint(0, attempted)
        monthly_progress.append({"date": date.strftime('%Y-%m-%d'), "attempted": attempted, "correct": correct})
    monthly_progress.reverse()

    # Simulated Improvement After AI-Generated Questions
    initial_score = 60  # Before AI-Generated Questions
    improved_score = 80  # After AI-Generated Questions

    context = {
        "total_attempted": total_attempted,
        "correct_answers": correct_answers,
        "incorrect_answers": incorrect_answers,
        "score": score,
        "weekly_progress": weekly_progress,
        "monthly_progress": monthly_progress,
        "initial_score": initial_score,
        "improved_score": improved_score
    }

    return render(request, "progress.html", context)
