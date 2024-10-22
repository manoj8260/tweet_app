from django.shortcuts import render
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
import os
# Create your views here.
def home(request):
      un=request.session.get('username')
      if un:
          UO=User.objects.get(username=un)
          PO = Profile.objects.get(username=UO)
          tweets=Tweet.objects.all()
          d={'UO':UO, 'PO': PO, 'tweets':tweets}
          return render(request,'home.html',d)
      tweets=Tweet.objects.all()
      d={'tweets':tweets}     
      return render(request,'home.html',d)

def register(request):
    ERFO=UserModel()
    EPFO=ProfileModel()
    d={'ERFO':ERFO,'EPFO':EPFO}
    if request.method == 'POST' and request.FILES:
        UFDO=UserModel(request.POST)
        PFDO=ProfileModel(request.POST,request.FILES)
        if UFDO.is_valid() and PFDO.is_valid():
            pw=UFDO.cleaned_data.get('password')
            MUFDO=UFDO.save(commit=False)
            MUFDO.set_password(pw)
            MUFDO.save()
            MPFDO=PFDO.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()
            return HttpResponseRedirect(reverse('user_login'))
        return HttpResponse('invalid data')
    return render(request,'register.html',d)

def user_login(request):
    if request.method == 'POST':
        un=request.POST.get('un')
        pw=request.POST.get('pw')
        AO=authenticate(username=un,password=pw)
        if AO:
          request.session['username']= un 
          login(request,AO)
          return HttpResponseRedirect(reverse('home'))
        return HttpResponse('user  not found')
    return render(request,'user_login.html')

def user_logout(request):
    logout(request)
    return HttpResponseRedirect('user_login')

def user_profile(request):
    un=request.session.get('username')
    if un:
     UO=User.objects.get(username=un)
     PO=Profile.objects.get(username=UO)
     d={'UO':UO,'PO':PO}
     return render(request,'home.html',d)    
    return render(request,'user_profile.html')

def create_tweet(request):
   ETFO=TweetModel() 
   d={'ETFO':ETFO}
   if request.method =='POST' and request.FILES:
       TFDO=TweetModel(request.POST,request.FILES)
       un=request.session.get('username')
       UO=User.objects.get(username=un)
       if UO:
           MTFDO=TFDO.save(commit=False)
           MTFDO.username= UO
           MTFDO.save()
           return  HttpResponseRedirect(reverse('home')) 
       return HttpResponse('invalid info ') 
   return render(request,'create_tweet.html',d)

def update(request,pk):
    TO=Tweet.objects.get(pk=pk)
    d={'TO':TO}
    if request.method == 'POST'and request.FILES:
        if TO.photo:
            os.remove(TO.photo.path)
        TO.text=request.POST.get('text')
        TO.photo=request.FILES.get('photo')
        TO.save()
        return HttpResponseRedirect(reverse('home'))    
    return render(request,'update.html',d)

def delete(request,pk):
    TO=Tweet.objects.get(pk=pk)
    if TO.username.username  == request.session.get('username'):
        TO.delete()
        return HttpResponseRedirect(reverse('home'))
    return HttpResponse('you dont delete other tweet')

def save(request,pk):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    TO=Tweet.objects.get(pk=pk)
    AST=Saved.objects.filter(tweet=TO)
    if AST and AST[0].username.username  == un:
        AST.delete()
        return HttpResponseRedirect(reverse('saved'))
    else:
        if  TO.username.username != un:
         save_tweet=Saved(username=UO,tweet=TO)
         save_tweet.save()
        return HttpResponseRedirect(reverse('saved')) 
    return HttpResponse('you dont save your tweet')

    
def saved(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)  
    ASO=Saved.objects.filter(username=UO)
    d={'tweets':ASO}
    return render(request,'saved.html',d)

def like(request,pk):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    TO=Tweet.objects.get(pk=pk)
    LO=Liked.objects.filter(username=UO,tweet=TO)
    if LO:
        TO.like -=1
        TO.save()
        LO.delete()
    else:
         TO.like +=1
         TO.save()
         LO=Liked(username=UO,tweet=TO)
         LO.save()
    return HttpResponseRedirect(reverse('home'))

def comment(request,pk):
    if request.method == 'POST':
        comment_text=request.POST.get('cmt')
        un=request.session.get('username')
        UO=User.objects.get(username=un)
        TO=Tweet.objects.get(pk=pk) 
        CO=Comment(username=UO,tweet=TO,comment_text=comment_text)
        CO.save()
        return HttpResponseRedirect('home')
    return render(request,'comment.html')

def commented(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    
    ACO=Comment.objects.filter(username=UO)
    d={'savecomment':ACO}
   
    
    return render(request,'save_comment.html',d)
        
    

