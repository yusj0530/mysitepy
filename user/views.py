from django.forms import model_to_dict
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from user.models import User


def joinform(request):
    return render(request, 'user/joinform.html')


def join(request):
    user = User()

    user.name  = request.POST['name']
    user.email = request.POST['email']
    user.password = request.POST['password']
    user.gender = request.POST['gender']

    # data_tuple = (name, email, password, gender)
    # models.insert(data_tuple)
    user.save()



    return HttpResponseRedirect('/user/joinsuccess')


def joinsuccess(request):
    return render(request, 'user/joinsuccess.html')

def loginform(request):
    return render(request, 'user/loginform.html')

def login(request):

    #user = models.get(email, password)
    results = User.objects.all().filter(email=request.POST['email']).filter(password=request.POST['password'])
    # email과 password 객체를 가져와 results에 담는다.
    print(results)

    #로그인 실패
    if len(results) == 0:
        return HttpResponseRedirect('/user/loginform?result=fail')

    #로그인 성공(처리)
    authuser = results[0]
    request.session['authuser'] = model_to_dict(authuser)
    #model_to_dict= 딕셔너리형태로 해줘야한다.(파이썬에서의 JSON형태/ JAVA에선 그냥 객체가 dict형태다.)

    #main으로 리다이렉트
    return HttpResponseRedirect('/')

def logout(request):
    del request.session['authuser']
    return  HttpResponseRedirect('/')

def modifyform(request):

    authuser = request.session['authuser']
    data = {'user': authuser}

    return render(request, 'user/modifyform.html', data)

def modify(request):

    #user = User.objects.get(email=request.GET['email'])
    authuser = request.session['authuser']
    auth = authuser['id']
    results=User.objects.all().filter(id=auth)
    user = results[0]

    user.password = request.POST['password']
    user.gender = request.POST['gender']
    user.save()

    return HttpResponseRedirect('/')

def checkemail(request):
    results = User.objects.filter(email = request.GET['email'])

    result = {'result' : len(results) == 0 } #True : not exist(사용가능)
    return JsonResponse(result)


def deleteform(request):

    authuser = request.session['authuser']
    data = {'user': authuser}

    return render(request, 'user/deleteform.html', data)



def delete(request):

    authuser = request.session['authuser']
    authid = authuser['id']
    authpass = authuser['password']
    password = request.POST['password']

    if password == authpass:
        User.objects.filter(id=authid).filter(password=password).delete()
        del request.session['authuser']

    return HttpResponseRedirect('/')

