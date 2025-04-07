from django.shortcuts import render, redirect
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

@login_required
def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'questions': questions})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            return redirect('home')
    else:
        print("I am here")
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

@login_required
def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', question_id=question_id)
    else:
        form = AnswerForm()
    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'form': form})

@login_required
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer.likes += 1
    answer.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
