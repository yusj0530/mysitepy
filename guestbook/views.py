from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from guestbook.models import Guestbook


def list(request):
    results = Guestbook.objects.all().order_by('-id')
    # data안에 빈공간이 없어야한다.
    data = {'guestbook_list':results}
    #data는 딕셔러니로 받아온다.
    #랜더링은 html로 바꾸는 과정이다.
    return render(request, 'guestbook/list.html', data)

def add(request):

    guestbook = Guestbook()

    guestbook.name = request.POST['name']
    guestbook.password = request.POST['pass']
    guestbook.content = request.POST['content']

    guestbook.save()

    # results = Guestbook.object.get(name = request.POST['name']).get(password=request.POST['pass']).get(content=request.POST['content'])
    # data = {'guestbook_list' : results }

    return HttpResponseRedirect('/guestbook')

def deleteform(request):

    id=request.GET['id']
    data ={'id':id}

    return render(request, 'guestbook/deleteform.html', data)

def delete(request):

    password= request.POST['password']
    id = request.POST['id']

    Guestbook.objects.filter(id=id).filter(password=password).delete()

    return HttpResponseRedirect('/guestbook')
