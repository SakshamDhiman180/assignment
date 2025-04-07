from django.shortcuts import render, redirect
from .models import Question, Answer, LikedAnswer
from .forms import QuestionForm, AnswerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from .serializer import get_serialized_answers
from django.contrib import messages

@login_required
def home(request):
    user = request.GET.get('user')
    if user == 'me':
        user_obj = request.user.id
        questions = Question.objects.filter(user=user_obj).order_by('-created_at')
    else:
        questions = Question.objects.all().order_by('-created_at')
    return render(request, 'home.html', {'data': questions, 'user': user or None, 'current_user': request.user})

@login_required
def post_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.save()
            messages.success(request, "Post created successfully!")
            return redirect('home')
    else:
        form = QuestionForm()
    return render(request, 'post_question.html', {'form': form})

@login_required
def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    answers = get_serialized_answers(request, answers)
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
    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'form': form, 'current_user': request.user})

@login_required
def delete_question(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.user == question.user:
        question.delete()
        messages.success(request, "Question deleted successfully!")
    return redirect('home')

@login_required
def delete_answer(request, answer_id):
    data = request.POST
    question_id = data.get('question_id') 
    answer = Answer.objects.get(id=answer_id)
    if request.user == answer.user:
        answer.delete()
        messages.success(request, "Answer deleted successfully!")
    return redirect('question_detail', question_id=question_id)

@login_required
def like_answer(request, answer_id):
    user = request.user
    if user:
        answer = Answer.objects.get(id=answer_id)
        liked_answer = LikedAnswer.objects.filter(user=user, answer=answer).first()
        if not liked_answer:
            LikedAnswer.objects.create(user=user, answer=answer)
            answer.likes += 1
        else:
            liked_answer.delete()
            
            answer.likes -= 1
        answer.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You are registered successfully, please login!")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
