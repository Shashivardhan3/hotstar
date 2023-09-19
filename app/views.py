from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'home.html')

def registration(request):
    umf=UserMF()
    pmf=ProfileMF()
    d={'pmf':pmf,'umf':umf}
    if request.method=="POST" and request.FILES:
        umfd=UserMF(request.POST)
        pmfd=ProfileMF(request.POST,request.FILES)
        if umfd.is_valid() and pmfd.is_valid():
            Nud=umfd.save(commit=False)
            submittedpw=umfd.cleaned_data['password']
            Nud.set_password(submittedpw)
            Nud.save()

            Npd=pmfd.save(commit=False)
            Npd.username=Nud
            Npd.save()

            send_mail('registartion','your Hotstar Registration Successfully completed....!',
                      'shashivardhan072@gmail.com',[Nud.email],fail_silently=False),
            return HttpResponse('data is submitted')

    return render(request,'registration.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST["username"]
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not active user')
    return render(request,'user_login.html')


@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    PO=Profile.objects.get(username=UO)

    d={'UO':UO,'PO':PO}
    return render (request,'display_profile.html',d)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def movies(request):
    return render(request,'movies.html')
def sports(request):
    return render(request,'sports.html')

@login_required
def change_password(request):
    if request.method=="POST":
        pw=request.POST['newpassword']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('PASSWORD CHANGED SUCCESSFULLY')
    return render (request,'change_password.html')

def reset_password(request):
    if request.method=='POST':
        password=request.POST['password']
        username=request.POST['username']
        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('Modify The password successfully')
        else:
            return HttpResponse('Username is not validate')
    return render(request,'reset_password.html')