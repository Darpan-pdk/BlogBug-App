
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from . import models
from .models import Posts
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError



def test(request):
    
    return render(request, 'blog/base.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def ulogin(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        password = request.POST.get('upassword')

        # Check if fields are empty
        if not name or not password:
            messages.error(request, "All fields are required!")
            return render(request, 'blog/ulogin.html', {'error': "All fields are required!"})

        userr = authenticate(request, username=name, password=password)

        if userr is not None:
            login(request, userr)
            
            # Clear old messages
            storage = messages.get_messages(request)
            storage.used = True  # Mark messages as used to prevent delay

            messages.success(request, "Login successful!")
            
            return redirect('/home')  # Redirect to home page after login
        else:
            messages.error(request, "Incorrect username or password. Please try again.")
            return render(request, 'blog/ulogin.html', {'error': "Incorrect username or password!"})

    return render(request, 'blog/ulogin.html')



def signup(request):
    if request.method == 'POST':
        name = request.POST.get('uname')
        email = request.POST.get('uemail')
        password = request.POST.get('upassword')

        # Check if any field is empty
        if not name or not email or not password:
            messages.error(request, "All fields are required!")
            return render(request, 'blog/signup.html', {'error': "All fields are required!"})

        try:
            # Try to create a new user
            newUser = User.objects.create_user(username=name, email=email, password=password)
            newUser.save()
            messages.success(request, "New user created! Redirecting to login page...")
            return render(request, 'blog/signup.html', {'redirect': True})  # Show success popup
        except IntegrityError:
            # Username already exists
            messages.error(request, "Username already exists. Please choose another one.")
            return render(request, 'blog/signup.html', {'error': "Username already exists!"})

    return render(request, 'blog/signup.html')

def home(request):
    context = {
        #'posts':Posts.objects.all() //shows posts in default order ie first posted first
        #new posted first 
        'posts': Posts.objects.all().order_by('-date_posted')
    }

    return render(request, 'blog/home.html', context)

def newpost(request):
    if request.method == 'POST':
        tittle = request.POST.get('tittle')
        content = request.POST.get('content')
        npost = models.Posts(tittle=tittle, content=content, author=request.user)
        npost.save()

        messages.success(request, "New Blog Posted! ")
        
        #time.sleep(1.5)
        return redirect('/newpost')


    return render(request, 'blog/newpost.html')


def mypost(request):
    context = {
        'posts': Posts.objects.filter(author = request.user).order_by('-date_posted')
        }
   

    return render(request, 'blog/mypost.html', context)


def signOut(request):
    logout(request)
    
    return redirect('/')



#function to delete post
def delete_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)
    
    # Check if the logged-in user is the author of the post
    if request.user == post.author:
        post.delete()
        messages.success(request, "Post deleted successfully!")
        
        return redirect('/mypost') #redirecting to mypost for immidiate popup message
    else:
        messages.error(request, "You are not authorized to delete this post.")

    return redirect('/mypost')

def update_post(request, post_id):
    post = get_object_or_404(Posts, id=post_id)

    if request.user != post.author:
        messages.error(request, "You are not authorized to update this post.")
        return redirect('/mypost')

    if request.method == 'POST':
        post.tittle = request.POST.get('tittle')
        post.content = request.POST.get('content')
        post.date_posted = timezone.now()  # Update time to current time
        post.save()

        messages.success(request, "Post updated successfully!")
        return redirect('/mypost')

    return render(request, 'blog/update_post.html', {'post': post})

    