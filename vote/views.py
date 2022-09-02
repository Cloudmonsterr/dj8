from django.shortcuts import render
from .models import Topic

# Create your views here.


def index(request):
    t = Topic.objects.all()
    context = {
        'tset' : t
    }
    return render(request, 'vote/index.html', context)

def detail(request, tpk):
    t = Topic.objects.get(id=tpk)
    c = t.choice_set.all()
    context = {
        't' : t,
        'cset' : c
    }
    return render(request, 'vote/detail.html', context)