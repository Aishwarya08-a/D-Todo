from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from todoapp.models import Todos
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def user_signup(request):
    context={}
    if request.method=="POST":
        uname=request.POST['uname'] 
        upass=request.POST['upass']
        cpass=request.POST['cpass']
        print(uname,upass,cpass)
    
        if uname == "" or upass == "" or cpass == "": 
            context['Errormsg'] = "Field cannot be empty"
            return render(request, 'signup.html', context)
        elif upass != cpass: 
            context['Errormsg'] = "Password did not match"
            return render(request, 'signup.html', context)
        else:
            try:
                u = User.objects.create(username=uname, email=uname, password=upass) 
                u.set_password(upass)
                u.save()
                context['Success'] = "User added successfully"
                return render(request, 'signup.html', context)
            except Exception:
                context['Errormsg'] = "Username already exists"
                return render(request, 'signup.html', context)
    else:
        return render(request, 'signup.html')
         
def user_login(request):
    context={}
    if request.method == "POST":
        uname = request.POST['uname'] 
        upass = request.POST['upass']
        if uname == "" or upass == "": 
            context['Errormsg'] = "Field cannot be empty"
            return render(request, 'login.html', context)
        else:
            u = authenticate(username=uname, password=upass)
            if u is not None:
                login(request, u)
                return redirect('/home') 
            else:
                context['Errormsg'] = "Invalid username and password"
                return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
    
@login_required(login_url='/login') 
def home(request):
    todos = Todos.objects.filter(user=request.user).order_by('-date')
    return render(request, 'home.html', {'todos': todos})

@login_required(login_url='/login')
def add(request):
    if request.method == "POST":
        title = request.POST['utitle']
        todo = Todos.objects.create(title=title, user=request.user)
        return redirect('/home')

@login_required(login_url='/login')
def delete(request, todo_id):
    todo = get_object_or_404(Todos, pk=todo_id)
    todo.delete()
    return redirect('/home')

@login_required(login_url='/login')
def complete(request, todo_id):
    todo = get_object_or_404(Todos, pk=todo_id)
    todo.completed = True
    todo.save()
    return redirect('/home')  
