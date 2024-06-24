from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login , logout , authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Joke
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already registered')
            elif User.objects.filter(username=username).exists():
                messages.warning(request, 'Username already registered')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account created successfully')
                    return redirect('dashboard')
                else:
                    messages.error(request, 'Authentication failed')
        else:
            messages.warning(request, 'Passwords do not match')
        
    return render(request, 'register.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request,username = username,password =  password)
        if user is not None:
            login(request=request, user = user)
            return redirect('dashboard')
        else:
            messages.warning(request=request,message=f'Username or password not match')
    return render(request,'login_view.html')


def logout_view(request):
    logout(request)
    return redirect('index')
    


def dashboard(request):
    joke = Joke.objects.filter(user = request.user).order_by('-id')
    context = {
        'jokes':joke
    }
    return render(request,'dashboard.html',context)


def add_joke(request):
    if request.method == 'POST':
        user = request.user
        content  = request.POST.get("content")
        Joke.objects.create(user = user, content = content)
        return redirect('dashboard')
    return render(request,'add_joke.html')


@login_required(login_url='login_view')
def edit_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id, user=request.user)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            joke.content = content
            joke.save()
            messages.success(request=request,message=f'Your Joke is successfully updated')
            return redirect(f'/view_joke/{joke_id}')
    return render(request, 'edit_joke.html', {'joke': joke})

@login_required(login_url='login_view')
def delete_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id, user=request.user)
    if request.method == "POST":
        joke.delete()
        messages.success(request=request,message=f'Your joke is deleted successfylly')
        return redirect(reverse('dashboard'))
    return render(request, 'delete_joke.html', {'joke': joke})



@login_required(login_url='login_view')
def view_joke(request, joke_id):
    joke = get_object_or_404(Joke, id=joke_id, user=request.user)
    return render(request, 'view_joke.html', {'joke': joke})
