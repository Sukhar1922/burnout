from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed

from .models import Questions

# Create your views here.

def test(request):
    return JsonResponse({'success': 'True'}, status=200)


def GETquestions(request):
    if request.method == 'GET':
        data = list(Questions.objects.values('id', 'Name_Question'))
        return JsonResponse(data, safe=False)

    return HttpResponseNotAllowed(['GET'])
