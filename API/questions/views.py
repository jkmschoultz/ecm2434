from database.models import Question, Answer, Achievement
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import redirect
import random
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

@csrf_exempt
def getQuestions(request):
    questions = list(Question.objects.all())
    size = len(questions)
    data = []
    list_of_questions = []
    while (len(list_of_questions) < 5) and (len(list_of_questions) < len(questions)):
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

class AuthGetQuestions(APIView):
    # Endpoint to get quiz questions for an authorised user
    permission_classes = [IsAuthenticated]

    # Register that bottle was filled by user
    def post(self, request):
        # Get username of authenticated user and redirect
        user = request.user
        # Get name of building that bottle is filled in
        building = ''
        try:
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            building = str( body_data.get('building'))
        except:
            building = str( request.POST['building'] )

        # Redirect to filling bottle in building
        # This will then redirect to getting quiz questions
        if building != '':
            return redirect('users:bottleFilled', current_username=user.username, building_name=building)
        else:
            return HttpResponseBadRequest('Must provide name of building bottle was filled in')