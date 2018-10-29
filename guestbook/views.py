from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
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

def ajax(request):
    return render(request, 'guestbook/ajax.html')

def api_list(request):
    p=request.GET['p']
    results_list=[]

    page = (int(p)-1) * 5
    results = Guestbook.objects.all().order_by('-id')[page:page+5]
    results_dict =results.values()

    for a in results_dict:
        results_list.append(a)

    data = {'result' : results_list}

    return JsonResponse(data)

def api_add(request):
    guestbook = Guestbook()

    guestbook.name = request.GET['name']
    guestbook.password = request.GET['pass']
    guestbook.content = request.GET['content']

    guestbook.save()

    response = {'result' : 'success', 'data': model_to_dict(guestbook) }

    return JsonResponse(response)