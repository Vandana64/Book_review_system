from django.shortcuts import render, redirect, get_object_or_404
from .models import book,review
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# --- LOGIN / SIGNUP ---

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def dashboard(request):
    total_books = book.objects.count()
    total_reviews = review.objects.count()  # total reviews in DB

    context = {
        'total_books': total_books,
        'total_reviews': total_reviews,
    }
    return render(request, 'dashboard.html', context)

@login_required(login_url='login')
def book_list(request):
    books = book.objects.all()
    return render(request, 'book_list.html', {'books': books})

@login_required(login_url='login')
def add_book(request):
    error = None
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        description = request.POST.get('description')
        published_date = request.POST.get('published_date')

        if title and author and description and published_date:
            book.objects.create(
                title=title,
                author=author,
                description=description,
                published_date=published_date
            )
            return redirect('book_list')
        else:
            error = "All fields are required."

    return render(request, 'add_book.html', {'error': error})

@login_required(login_url='login')
def edit_book(request, id):
    bk = get_object_or_404(book, id=id)

    if request.method == 'POST':
        bk.title = request.POST['title']
        bk.author = request.POST['author']
        bk.description = request.POST['description']
        bk.published_date = request.POST['published_date']
        bk.save()
        return redirect('book_list')

    return render(request, 'edit_book.html', {'book': bk})

@login_required(login_url='login')
def delete_book(request, id):
    bk = get_object_or_404(book, id=id)
    bk.delete()
    return redirect('book_list')
@login_required(login_url='login')
def add_review(request, book_id):
    bk = get_object_or_404(book, id=book_id)
    
    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")
        review.objects.create(book=bk, user=request.user, rating=rating, comment=comment)
        return redirect("book_list")
    
    return render(request, "add_review.html", {"book": bk})

def review_list(request):
    reviews = review.objects.all()
    total_books = book.objects.count()
    total_reviews = reviews.count()
    return render(request, 'review_list.html', {
        'reviews': reviews,
        'total_books': total_books,
        'total_reviews': total_reviews
    })
