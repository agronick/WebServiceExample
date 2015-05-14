from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from questions.models import Question, Answer
import simplejson as json
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt


post_error = 'Expected a post request'

def index(request):
    return HttpResponse("/questions - question list")

@csrf_exempt
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

@csrf_exempt
def update(request, id):
    if request.method != 'POST':
        return return_json(post_error, 400)


    question_text, answers, correct_index = edit_post_vars(request)

    q = Question.objects.get(pk=id)
    q.question = question_text
    q.save()

    q.answer_set.all().delete()

    i=0;
    for answer in answers:
        a = Answer(question=q, choice=answer, correct=(i == correct_index))
        a.save()
        i += 1

    data = {
        'result': 'success',
        'id': id,
    }
    json_result = json.JSONEncoder().encode(data)
    return return_json(json_result)

@csrf_exempt
def new(request):
    if request.method != 'POST':
        return return_json(post_error)

    question_text, answers, correct_index = edit_post_vars(request)

    q = Question(question=question_text)
    q.save()

    i = 0;
    for answer in answers:
        a = Answer(question=q, choice=answer, correct=(i == correct_index))
        a.save()
        i += 1

    data = {
        'result': 'success',
        'id': q.id
    }
    json_result = json.JSONEncoder().encode(data)
    return HttpResponse(json_result, content_type="application/json")

def edit_post_vars(request):
    question_text = request.POST.get('question', '')
    answers = request.POST.getlist('answers[]')
    correct_index =  int(request.POST.get('correct', ''))
    return question_text, answers, correct_index

@csrf_exempt
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

    correct = Answer.objects.filter(question=key, correct=True).values('choice', 'id')
    wrong_ans = {}
    wrong = Answer.objects.filter(question=key, correct=False).values('choice', 'id')
    for i in wrong:
        wrong_ans[i['id']] = i['choice']


    question = {
        'id': q_model.id,
        'question': q_model.question,
        'wrong_answers': wrong_ans,
    }

    question['correct_answer'] = {}

    if correct:
        question['correct_answer'] = {correct[0]['id']: correct[0]['choice']}


    return question

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False