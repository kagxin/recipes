from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from app.models import Person
import json

# Create your views here.
class BaseView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(BaseView, self).dispatch(request, *args, **kwargs)


class PersionView(BaseView):

    def get(self, request, *args, **kwargs):
        wrap_person = lambda p : {'id':p.id, 'name':p.name, 'age':p.age}
        data = list(map(wrap_person, Person.objects.all()))
        return JsonResponse(data, safe=False, status=200)

    def post(self, request, *args, **kwargs):
        status = 200
        message = ''
        try:
            data = json.loads(request.body.decode('utf-8'))
            assert 'age' in data.keys(), 'no age'
            assert 'name' in data.keys(), 'no name'
            Person.objects.create(name = data['name'], age=data['age'])
            message = 'ok'
        except (json.decoder.JSONDecodeError):
            status = 400
            message = 'check json format.'
        except AssertionError as e:
            status = 400
            message = str(e)

        return JsonResponse({'message':message}, safe=False, status=status)
