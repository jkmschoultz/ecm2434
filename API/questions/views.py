from database.models import Question, Answer, Achievement
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def getQuestions(request):
    questions = list(Question.objects.all())
    size = len(questions)
    data = []
    list_of_questions = []
    while (len(list_of_questions) < 5) and (len(list_of_questions) < len(questions)):
        print(len(list_of_questions))
        question_num = random.randint(0,size-1)
        if question_num not in list_of_questions:
            list_of_questions.append(question_num)
            question = questions[question_num]
            question_text = questions[question_num].text
            anwsers_list = list(Answer.objects.filter(question = question))
            anwsers = []
            for anwser in anwsers_list:
                anwsers.append({'text':anwser.text,'correct':anwser.is_correct})
            data.append({'text': question_text, 'answers': anwsers})
    return JsonResponse({'data':data})