from django.urls import path

from . import views

# App for handling user quiz interaction
app_name = 'quiz'
urlpatterns = [
    path('', views.LogAnswers.as_view(), name='answer_quiz')
]