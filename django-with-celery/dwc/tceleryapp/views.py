from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.generic import View
from .tasks import add
from celery import group
from .models import Persion

# Create your views here.
class TestView(View):

    def get(self, *args, **kwargs):
        res = group(add.s(i, i) for i in range(10)).delay()
        data = res.get()
        import json
        return HttpResponse(json.dumps(data))