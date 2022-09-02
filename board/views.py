from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
# Create your views here.


def index(request):
    cate = request.GET.get("cate", "")
    kw = request.GET.get("kw", "")
    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith= kw)
        elif cate == "con":
            b = Board.objects.filter(content__contains= kw)
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer= u)
            except:
                b = Board.objects.none()
    else:
        b = Board.objects.all()

    b = b.order_by('pubdate')
    pg = request.GET.get("page", 1)
    pag = Paginator(b,10)
    obj = pag.get_page(pg)
    context = {
        "bset" : obj,
        "cate" : cate,
        "kw" : kw
    }
    return render(request, 'board/index.html', context)

def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    context = {
        'b' : b,
        'rset' : r
    }
    return render(request, 'board/detail.html', context)

def delete(request, bpk):
    b = Board.objects.get(id = bpk)
    if  b.writer == request.user:
        b.delete()
    else:
        pass # 메세지
    return redirect('board:index')

def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        w = request.user
        c = request.POST.get("con")
        d = timezone.now()
        Board(subject = s, writer = w, content = c, pubdate = d).save()
        return redirect('board:index')
    return render(request, 'board/create.html')

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    context = {
        'b' : b
    }
    if b.writer != request.user:
        # 메세지
        return redirect('board:index')

    if request.method == "POST":
        s = request.POST.get("nsub")
        c = request.POST.get("ncon")
        b.subject, b.content = s, c
        b.save()
        return redirect('board:detail', bpk)
    return render(request, 'board/update.html', context)

def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    print(c)
    Reply(board=b, comment =c, replyer=request.user).save()
    return redirect('board:detail', bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        pass # 마지막날 메시지
    return redirect("board:detail", bpk)