from django.shortcuts import render_to_response
from models import TestForm

def test(request):
    f = TestForm()
    return render_to_response('test.html', {'f' : f})
