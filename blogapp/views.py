from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Post,Like,Comment
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
# Create your views here.
def error_page(request,exception):
    return render(request,'404.html')

def index(request):
    posts = Post.objects.all()
    user = request.user
    context = {
        'posts':posts,
        'user':user,
    }
    return render(request,'home.html',context)

def search(request):
    if request.method == "POST":
        srh = request.POST["srh"]
        if srh:
            srch = Post.objects.filter( Q(title__icontains = srh) )
            if srch:
                return render(request,'home.html',{"search":srch})
            else:
                posts = Post.objects.all()
                user = request.user
                context = {
                    'posts':posts,
                    'user':user,
                }
                messages.error(request,"No Results Found")
                return render(request,"home.html",context)
        else:
            return redirect('/')
    return render(request,'home.html')

def register(request):
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        if password == confirm_password:
            if User.objects.filter(email=email).exists():
                messages.error(request,"email already exists")
                return render(request,'register.html')
            if User.objects.filter(username=username).exists():
                messages.error(request,"username already exists")
                return render(request,'register.html')
            else:
                user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username,password=password)
                user.save()
                messages.success(request,'user registered successfully')
                return redirect("/login")
        else:
            messages.error(request,"password and confirm password not matching")
            return render(request,'register.html')
    else:
        return render(request,'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        nextvalue = request.POST["next"]
        user = auth.authenticate(username=username,password=password)
        if user is not None and nextvalue == "":
            auth.login(request,user)
            messages.success(request,"logged in successfully")
            return redirect("/")
        elif user is not None and nextvalue:
            auth.login(request,user)
            return redirect(nextvalue)
        else:
            messages.error(request,"username and password is not valid")
            return redirect("/login")
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request,"logged out successfully")
    return redirect("/")

def profile(request):
    user = request.user
    liked = Post.objects.filter(liked=user)
    return render(request,'profile.html',{'liked':liked})

def adminpage(request):
    posts = Post.objects.all()
    return render(request,'admin.html',{'posts':posts})

def edit_post(request,id):
    post = Post.objects.get(post_id=id)
    if request.method == "POST":
        if request.user.is_staff:
            post.title = request.POST["title"]
            post.description = request.POST["description"]
            post.author = request.user
            post.save()
            messages.success(request,"Post updated successfully")
            return redirect("/")
        else:
            return HttpResponse(status=404)
    return render(request,'edit_post.html',{'post':post})

@login_required(login_url="login")
def post_details(request,id):
    post = Post.objects.get(post_id=id)
    return render(request,'post_details.html',{'post':post})

def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request,"Password change successfully")
            auth.logout(request)
            return redirect("/login")
        else:
            messages.error(request,"please make sure below constraints are satisfied to change the password")
            return redirect("change_password")
    else:
        form = PasswordChangeForm(request.user)
        return render(request,'change_password.html', {'form':form})

def post(request):
    if request.method == "POST":
        if request.user.is_staff:
            title = request.POST["title"]
            description = request.POST["description"]
            author = request.user
            post = Post.objects.create(title=title,description=description,author=author)
            post.save()
            messages.success(request,"Post Saved Successfully")
            return redirect("/")
        else:
            messages.success(request,"You don't have permission to post article")
            return redirect("/")
    else:
        return render(request,'post.html')

def like_post(request,id):
    user = request.user
    post_obj = Post.objects.get(post_id=id)
    if user in post_obj.liked.all():
        post_obj.liked.remove(user)
    else:
        post_obj.liked.add(user)

    like,created = Like.objects.get_or_create(post=post_obj,user=user)
    if not created:
        if like.value == 'Like':
            like.value="Unlike"
        else:
            like.value="Like"
    like.save()
    return redirect("/")

def comment_post(request,id):
    if request.method == "POST": 
        user = request.user
        post_obj = Post.objects.get(post_id=id)
        content = request.POST['content']
        if user not in post_obj.comments.all():
            post_obj.comments.add(user)

        comment,created = Comment.objects.get_or_create(post=post_obj,user=user)
        if not created:
            comment.post = post_obj
            comment.user = user
            comment.content = content
            comment.save()
            messages.success(request,"Comment updated successfully")
            return redirect("/")
        comment.content = content
        comment.save()
        messages.success(request,"Comment saved successfully")
        return redirect("/")
    else:
        post_obj = Post.objects.get(post_id=id)
        return render(request,"comment_post.html",{'post':post_obj})
