from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from questions.models import Question, Answer
import logging
import simplejson as json
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger('django')

post_error = 'Expected a post request'

def index(request):
    return HttpResponse("/questions - question list")

def list(request):

    per_page = int(request.POST.get('per_page', 10))
    offset = int(request.POST.get('start_page', 1)) - 1;
    offset = int(offset) * per_page
    order = '-' if (request.POST.get('sort', 'des') == 'des') else ''
    search = request.POST.get('search', '')

    end_offset = offset + per_page;

    questions = []
    ids = Question.objects.values('id').filter(question__contains=search).order_by(order + 'question')[offset:end_offset]
    for id in ids:
        questions.append(questions_with_answer(id['id']))


    json_result = json.JSONEncoder().encode(questions)
    return return_json(json_result)

def single(request, id):
    try:
        questions = questions_with_answer(id)
    except ObjectDoesNotExist:
        return return_json('Could not find question with id ' + id, 404)

    json_result = json.JSONEncoder().encode(questions)
    return return_json(json_result)

def update(request, id):
    if request.method != 'POST':
        return return_json(post_error, 400)

    try:
        question = Question.objects.get(id)
    except ObjectDoesNotExist:
        return return_json('Could not find question with id ' + id, 404)

def new(request):
    if request.method != 'POST':
        return return_json(post_error, 400)

    question_text = request.POST.get('question', '')
    answers = request.POST.get('answers', [])
    correct_index = request.POST.get('correct', '')

    q = Question(question=question_text)
    q.save()

    i = 0;
    for answer in answers:
        a = Answer(question=q, choice=answer, correct=(i == correct_index))
        a.save()
        ++i

    data = {
        'result': 'success',
        'data': q.id
    }
    json_result = json.JSONEncoder().encode(data)
    return HttpResponse(json_result, content_type="application/json")

def delete(request):
    if request.method != 'POST':
        return return_json(post_error, 400)

    id = request.POST.get('id', '')
    if not id or not is_number(id):
        return return_json('Missing question ID', 400)

    question = Question.objects.get(pk=id)
    question.delete()

    data = {
        'result': 'success',
        'data': question.id
    }
    json_result = json.JSONEncoder().encode(data)
    return return_json(json_result)


def return_json(result, code = 200):
    if code == 200:
        return HttpResponse(result, content_type="application/json")

    #errors
    output = {
        'error_code': code,
        'result': result
    }

    if code == 404:
        return HttpResponseNotFound(json.JSONEncoder().encode(output), content_type="application/json")
    elif code == 400:
        return HttpResponseBadRequest(json.JSONEncoder().encode(output), content_type="application/json")

def questions_with_answer(key):
    q_model = Question.objects.get(pk=key)


    correct = Answer.objects.filter(question=key, correct=True).values('choice', 'id');
    wrong_ans = {}
    wrong = Answer.objects.filter(question=key, correct=False).values('choice', 'id')
    for i in wrong:
        wrong_ans[i['id']] = i['choice']


    answer = {}

    if (correct.count()):
        answer.correct['id'] = correct['choice']


    question = {
        'id': q_model.id,
        'question': q_model.question,
        'correct_answer': answer,
        'wrong_answers': wrong_ans
    }
    return question

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False