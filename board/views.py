from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from board import models

def api_list(request):
    page=request.GET['p']
    results = models.fetchList(page)

    response = {'result': 'success', 'data':results}
    return JsonResponse(response)



def list(request):

    results = models.fetchall()
    count = len(results)

    for result in results:
        result['list_no']=count
        count-=1

    data = {'board_list': results}
    return render(request, 'board/list.html', data)

def view(request):
    id = request.GET['id']
    results = models.fetchone(int(id))
    data = {'boardview': results}
    models.hitupdate(id)

    return render(request, 'board/view.html',data)

def delete(request):

    id = request.GET['id']
    authuser = request.session['authuser']
    authid = authuser['name']

    models.delete((int(id), authid))

    return HttpResponseRedirect('/board')

def write(request):

    return render(request, 'board/write.html')

def replywrite(request):

    id = request.GET['id']
    results = models.fetchone(id)
    data = {'write': results}
    return render(request, 'board/reply.html', data)

def add(request):


    title = request.POST['title']
    content = request.POST['content']
    authuser = request.session['authuser']
    authid = authuser['name']

    models.insert(( title, content, authid))

    return HttpResponseRedirect('/board')

def replyform(request):
    id = request.GET['id']
    data = {'id':str(id)}
    results = models.fetchone(int(id))
    dd ={'data':results}
    order_no = dd['data']['order_no']
    group_no = dd['data']['group_no']
    models.re_update(int(order_no), int(group_no))

    return render(request, 'board/reply.html', data)

def reply(request):

    id = request.GET['id']
    title = request.POST['title']
    content = request.POST['content']
    authuser = request.session['authuser']
    authid = authuser['name']

    results = models.fetchone(int(id))
    data = {'id': results}
    group_no=data['id']['group_no']
    order_no = data['id']['order_no']
    depth = data['id']['depth']

    models.insert1((title, content, int(group_no), int(order_no)+1, int(depth)+1, authid ))

    return HttpResponseRedirect('/board')


def modify(request):
    id = request.GET['id']
    results = models.fetchone(int(id))
    data = {'boardview':results}

    return render(request, 'board/modify.html', data)

def view_modify(request):

    title = request.POST['title']
    content = request.POST['content']
    id =int(request.GET['id'])

    models.update(title, content, int(id))

    return HttpResponseRedirect('/board/view?id='+str(id))

def api_list(request):
    page = request.GET['p']
    results = models.fetchList(page)

    response = {'result':'success', 'data':results}
    return JsonResponse(response)