from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

User = get_user_model()


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)

            if user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('student_dashboard')

        return render(request, 'auth/login.html', {
            'error': 'Invalid username or password'
        })

    return render(request, 'auth/login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not username or not email or not password or not confirm_password:
            return render(request, 'auth/register.html', {
                'error': 'All fields are required'
            })

        if password != confirm_password:
            return render(request, 'auth/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=username).exists():
            return render(request, 'auth/register.html', {
                'error': 'Username already exists'
            })

        # ✅ create student user using CUSTOM user model
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = False   # student
        user.is_active = True
        user.save()

        return redirect('login')

    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    return redirect('login')
