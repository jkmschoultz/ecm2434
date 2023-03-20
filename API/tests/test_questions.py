from database.models import *
from django.test import TestCase, Client

class TestQuestions(TestCase):
    def setUp(self):
        question = Question.objects.create(text='Test question')
        answer1 = Answer.objects.create(text = 'this is false', question = question, is_correct = False)
        answer2 = Answer.objects.create(text = 'this maybe false', question = question, is_correct = False)
        answer3 = Answer.objects.create(text = 'this is true', question = question, is_correct = True)
        answer4 = Answer.objects.create(text = 'this isnt not false', question = question, is_correct = False)

    # Clean up run after every test method    
    def tearDown(self):
        pass

    def testGetQuestions(self):
        # Test that to see if the endpoint recieves questions for a test
        c = Client()
        response = c.get('/questions/')
        data = response.json()
        self.assertEqual(len(data['data']), 1)
        self.assertEqual(data['data'][0]['text'], 'Test question')
        self.assertEqual(len(data['data'][0]['answers']), 4)
        answers = data['data'][0]['answers']
        for answer in answers:
            if answer['correct'] == True:
                self.assertEqual(answer['text'], 'this is true')