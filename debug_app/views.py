from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import ErrorSolutionForm
from .models import ErrorSolution
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q


# Landing page (public)
def landing(request):
    return render(request, "debug_app/landing.html")


# Dashboard
@login_required
def home(request):
    query = request.GET.get('q', '').strip()
    tag = request.GET.get('tag')

    errors = ErrorSolution.objects.filter(user=request.user)

    if query:
        errors = errors.filter(
            Q(error_title__icontains=query) |
            Q(error_description__icontains=query) |
            Q(tags__name__icontains=query)   
        )

    if tag:
        errors = errors.filter(tags__name__icontains=tag)  
    errors = errors.distinct()  
    return render(request, "debug_app/home.html", {"errors": errors})


# Add Error
@login_required
def add_error(request):
    if request.method == "POST":
        form = ErrorSolutionForm(request.POST)

        if form.is_valid():
            form.save(user=request.user) 
            return redirect('home')
    else:
        form = ErrorSolutionForm()

    return render(request, "debug_app/add_error.html", {"form": form})


# Edit Error
@login_required
def edit_error(request, id):
    error = get_object_or_404(ErrorSolution, id=id, user=request.user)

    if request.method == "POST":
        form = ErrorSolutionForm(request.POST, instance=error)

        if form.is_valid():
            form.save(user=request.user)  
            return redirect('home')
    else:
        tags = ", ".join(tag.name for tag in error.tags.all())

        form = ErrorSolutionForm(
            instance=error,
            initial={'tags': tags}
        )

    return render(request, "debug_app/edit_error.html", {"form": form})


# Login
def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "debug_app/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "debug_app/login.html")


# Register
def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Validation
        if password != confirm_password:
            return render(request, "debug_app/register.html", {
                "error": "Passwords do not match"
            })

        if User.objects.filter(username=username).exists():
            return render(request, "debug_app/register.html", {
                "error": "Username already exists"
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, "debug_app/register.html")


# Logout
def user_logout(request):
    logout(request)
    return redirect('landing')


# Delete Error (SAFE)
@login_required
def delete_error(request, id):
    error = get_object_or_404(ErrorSolution, id=id, user=request.user)

    if request.method == "POST":  
        error.delete()

    return redirect('home')