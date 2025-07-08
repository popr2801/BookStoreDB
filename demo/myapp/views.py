from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
from .models import Book,User
from .forms import UserForm,LoginForm
from django.contrib.auth.hashers import make_password,check_password
from django.db import connection

def home(request):
   return render(request,"index.html")



def book_list(request):
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        if book_id:
            try:
                book = Book.objects.get(bookid = book_id)
                if book.stoc > 0:
                    book.stoc -= 1
                    book.save()
            except Book.DoesNotExist:
                pass
        return redirect("book_list")
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def user_list(request):
    users = User.objects.all()
    return render(request,'user_list.html',{'users' : users})

def register(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.passwordhash = make_password(form.cleaned_data["password"])
            user.save()
            return HttpResponse("Profile Saved!")
    else:
        form = UserForm()
    return render(request,'register.html',{'form':form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if check_password(password,user.passwordhash):
                    request.session['user_id'] = user.userid
                    return redirect("user_home")
                else:
                    messages.error(request,"Invalid Password")
            except User.DoesNotExist:
                messages.error(request,"User not found")
    else:
        form = LoginForm()
    return render(request,'login.html',{'form' : form})

def buy_book(user_id,book_id):
    with connection.cursor() as cursor:
        cursor.execute("EXEC BuyBook @UserId = %s, @BookID = %s",[user_id,book_id])

def owned_books(user_id):
    with connection.cursor() as cursor:
        cursor.execute("SELECT BookID, Title, Author, Description, MIN(BuyingDate) AS BuyingDate FROM OwnedBooks WHERE UserID = %s GROUP BY BookID, Title, Author, Description",[user_id])
        rows = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns,row)) for row in rows]
    

def user_home(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login")
    user = User.objects.get(userid = user_id)
    books = owned_books(user_id)
    return render(request,'user_home.html',{"user" : user , "owned_books" : books})

def logout(request):
    request.session.flush()
    return redirect('home')

def browse_books(request):
    user_id = request.session.get("user_id")
    user = User.objects.get(pk=user_id)
    if request.method == "POST":
        book_id = request.POST.get("book_id")
        if book_id:
            try:
                book = Book.objects.get(bookid = book_id)
                if book.stoc <= 0:
                    messages.error(request, "There are no more books!")
                elif user.balance < book.price:
                    messages.error(request, "Insufficient funds!")
                else:
                    book.stoc -= 1
                    book.save()
                    user.balance -= book.price
                    user.save()
                    buy_book(user_id,book_id)
                    messages.success(request, f'You bought "{book.title}"')
            except Book.DoesNotExist:
                pass
        return redirect("browse_books")
    books = Book.objects.all()
    return render(request, 'browse_books.html', {'user': user, 'books': books})

