from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('post/', views.post_question, name='post_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
    path('signup/', views.signup, name='signup'),
]
